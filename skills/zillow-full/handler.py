"""
zillow-full skill handler — calls the Zillapi REST API.

Pure standard library. No third-party dependencies.
Auth: bearer token in `ZILLAPI_KEY` env var.
Errors are returned as {"error": "...", "detail": "..."} dicts rather than raised.
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://api.zillapi.com/v1"
USER_AGENT = "zillow-skills/1.0.1 (+https://github.com/nikhonit/zillow-skills)"
TIMEOUT_SECONDS = 30


def _key():
    k = os.environ.get("ZILLAPI_KEY", "").strip()
    if not k:
        raise RuntimeError(
            "ZILLAPI_KEY environment variable is not set. "
            "Get a free key in 30 seconds at https://zillapi.com/signup "
            "(100 credits, no card required). Then export ZILLAPI_KEY=zk_..."
        )
    return k


def _request(method, path, params=None, body=None):
    try:
        url = API_BASE + path
        if params:
            filtered = {k: v for k, v in params.items() if v is not None}
            if filtered:
                url = url + "?" + urllib.parse.urlencode(filtered)
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Authorization": "Bearer " + _key(),
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        try:
            detail = e.read().decode("utf-8")[:1000]
        except Exception:
            detail = ""
        return {"error": "HTTP " + str(e.code), "detail": detail}
    except urllib.error.URLError as e:
        return {"error": "network", "detail": str(e.reason)}
    except RuntimeError as e:
        return {"error": "auth", "detail": str(e)}
    except Exception as e:
        return {"error": "unexpected", "detail": str(e)}


def lookup_property_by_address(address, status="FOR_SALE", fields=None):
    """
    Look up a U.S. property by address.

    address: street address string, minimum 6 characters.
    status:  FOR_SALE | RECENTLY_SOLD | FOR_RENT (default FOR_SALE).
    fields:  optional comma-separated dotted-path projection (e.g. "zpid,price,zestimate").
    """
    return _request(
        "GET",
        "/properties/by-address",
        params={"address": address, "status": status, "fields": fields},
    )


def lookup_property_by_url(url, status="FOR_SALE", extract_units="disabled", fields=None):
    """
    Look up a property by its Zillow.com URL.

    extract_units: disabled | all | for_sale | for_rent | recently_sold | off_market.
                   Use "all" to also pull unit lists when the URL points at a multi-unit building.
    """
    return _request(
        "GET",
        "/properties/by-url",
        params={
            "url": url,
            "status": status,
            "extract_units": extract_units,
            "fields": fields,
        },
    )


def lookup_property_by_zpid(zpid, fields=None):
    """Look up a property by Zillow zpid. Cache-served when fresh."""
    return _request(
        "GET",
        "/properties/" + str(zpid),
        params={"fields": fields},
    )


def get_zestimate(zpid=None, address=None):
    """
    Get the Zestimate, rent Zestimate, tax assessed value, and last-sold price.

    Pass either zpid (preferred — cheaper) or address. If only address is given,
    the handler resolves the zpid first, then calls the dedicated zestimate endpoint.
    """
    if not zpid and not address:
        return {"error": "invalid_argument", "detail": "Provide either zpid or address"}
    if not zpid:
        record = _request(
            "GET",
            "/properties/by-address",
            params={"address": address, "fields": "zpid"},
        )
        if "error" in record:
            return record
        zpid = (record.get("data") or {}).get("zpid")
        if not zpid:
            return {"error": "not_found", "detail": "Could not resolve a zpid for that address"}
    return _request("GET", "/properties/" + str(zpid) + "/zestimate")


def search_listings(
    location=None,
    bbox=None,
    status="for_sale",
    price_min=None,
    price_max=None,
    beds_min=None,
    beds_max=None,
    baths_min=None,
    baths_max=None,
    sqft_min=None,
    sqft_max=None,
    year_built_min=None,
    year_built_max=None,
    home_types=None,
    days_on_zillow=None,
    max_items=50,
):
    """
    Search active listings.

    Pass either `location` (city, ZIP, neighborhood string) OR `bbox`
    ("west,south,east,north" decimal degrees). status: for_sale | for_rent | sold.
    home_types: comma-separated subset of {house, condo, townhouse, multi_family,
    manufactured, lot, apartment}. days_on_zillow: one of "1","7","14","30","90",
    "6m","12m","24m","36m". max_items capped at 50 per call.
    """
    return _request(
        "GET",
        "/listings",
        params={
            "status": status,
            "location": location,
            "bbox": bbox,
            "price_min": price_min,
            "price_max": price_max,
            "beds_min": beds_min,
            "beds_max": beds_max,
            "baths_min": baths_min,
            "baths_max": baths_max,
            "sqft_min": sqft_min,
            "sqft_max": sqft_max,
            "year_built_min": year_built_min,
            "year_built_max": year_built_max,
            "home_types": home_types,
            "days_on_zillow": days_on_zillow,
            "max_items": max_items,
        },
    )


def get_price_history(zpid=None, address=None):
    """Get price and listing-status history for a property."""
    zpid = _resolve_zpid(zpid, address)
    if isinstance(zpid, dict):
        return zpid
    return _request("GET", "/properties/" + str(zpid) + "/price-history")


def get_property_photos(zpid=None, address=None):
    """Get the photo gallery for a property."""
    zpid = _resolve_zpid(zpid, address)
    if isinstance(zpid, dict):
        return zpid
    return _request("GET", "/properties/" + str(zpid) + "/photos")


def get_property_schools(zpid=None, address=None):
    """Get assigned schools and GreatSchools ratings for a property."""
    zpid = _resolve_zpid(zpid, address)
    if isinstance(zpid, dict):
        return zpid
    return _request("GET", "/properties/" + str(zpid) + "/schools")


def get_listing_agent(zpid=None, address=None):
    """Get the listing agent and broker contact for an active listing."""
    zpid = _resolve_zpid(zpid, address)
    if isinstance(zpid, dict):
        return zpid
    return _request("GET", "/properties/" + str(zpid) + "/agent")


def _resolve_zpid(zpid, address):
    if zpid:
        return zpid
    if not address:
        return {"error": "invalid_argument", "detail": "Provide either zpid or address"}
    record = _request(
        "GET",
        "/properties/by-address",
        params={"address": address, "fields": "zpid"},
    )
    if "error" in record:
        return record
    resolved = (record.get("data") or {}).get("zpid")
    if not resolved:
        return {"error": "not_found", "detail": "Could not resolve a zpid for that address"}
    return resolved
