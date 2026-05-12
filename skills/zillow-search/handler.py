"""
zillow-search skill handler — listing search via the Zillapi REST API.

Pure standard library. Bearer token in ZILLAPI_KEY.
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://api.zillapi.com/v1"
USER_AGENT = "zillow-skills/1.0.0 (+https://github.com/nikhonit/zillow-skills)"
TIMEOUT_SECONDS = 30


def _key():
    k = os.environ.get("ZILLAPI_KEY", "").strip()
    if not k:
        raise RuntimeError(
            "ZILLAPI_KEY environment variable is not set. "
            "Get a free key with 100 credits at https://zillapi.com/signup"
        )
    return k


def _request(path, params=None):
    try:
        url = API_BASE + path
        if params:
            filtered = {k: v for k, v in params.items() if v is not None}
            if filtered:
                url = url + "?" + urllib.parse.urlencode(filtered)
        req = urllib.request.Request(
            url,
            method="GET",
            headers={
                "Authorization": "Bearer " + _key(),
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

    location: city, ZIP, neighborhood string (e.g. "Austin, TX")
    bbox:     "west,south,east,north" decimal degrees (alternative to location)
    status:   for_sale | for_rent | sold (default for_sale)

    Either location or bbox is required. Returns:
        {"data": [<listing>, ...], "meta": {"count": N}}
        or {"error": "...", "detail": "..."}
    """
    if not location and not bbox:
        return {"error": "invalid_argument", "detail": "Provide either location or bbox"}
    return _request(
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
