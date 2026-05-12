"""
zillow-zestimate skill handler — single-purpose Zestimate lookups.

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


def get_zestimate(zpid=None, address=None):
    """
    Get the Zestimate, rent Zestimate, tax assessed value, and last-sold price.

    Pass either zpid (preferred — cheaper) or address. If only address is given,
    the handler resolves the zpid first, then calls the dedicated zestimate endpoint.

    Returns:
        {"data": {"zestimate": ..., "rent_zestimate": ..., "tax_assessed_value": ...,
                  "last_sold_price": ..., "currency": "USD"}}
        or {"error": "...", "detail": "..."} on failure.
    """
    if not zpid and not address:
        return {"error": "invalid_argument", "detail": "Provide either zpid or address"}
    if not zpid:
        record = _request("/properties/by-address", params={"address": address, "fields": "zpid"})
        if "error" in record:
            return record
        zpid = (record.get("data") or {}).get("zpid")
        if not zpid:
            return {"error": "not_found", "detail": "Could not resolve a zpid for that address"}
    return _request("/properties/" + str(zpid) + "/zestimate")
