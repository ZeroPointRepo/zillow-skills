---
name: zillow-full
version: 1.1.0
description: Complete Zillow property data toolkit via the zillapi API. Looks up any US property by address, zillow.com URL or zpid and returns price, Zestimate, rent Zestimate, photos, schools, taxes, price history and listing agent contact; also searches for sale, for rent and sold listings by location and filters. Use when the user asks about a specific US property, home values, Zestimates, real estate listings, rentals, comps or housing data, or pastes a zillow.com link and asks about it. Do not use when an address appears incidentally (signatures, unrelated documents) or the conversation is abstract real estate talk with no specific property or search request.
license: MIT-0
author: Zero Point Studio
homepage: https://zillapi.com
repository: https://github.com/ZeroPointRepo/zillow-skills
tags:
  - zillapi
  - zillow
  - real-estate
  - property-data
  - zestimate
  - listings
  - search
  - api
metadata:
  openclaw:
    primaryEnv: ZILLAPI_KEY
    homepage: https://zillapi.com
    requires:
      env:
        - ZILLAPI_KEY
---

# zillow-full

Nine tools over the Zillapi REST API. Every call consumes credits, so fire only when the request is genuinely about a specific property or listing search. When intent is ambiguous, confirm with the user before calling.

## Tools

| Tool | Credits | Use for |
|---|---|---|
| `lookup_property_by_address` | 1 | Full record from a US address (loose strings work, 6+ chars) |
| `lookup_property_by_url` | 1 | Full record from a pasted `zillow.com/homedetails/...` link |
| `lookup_property_by_zpid` | 1 | Full record when the zpid is already known (cache-served when fresh) |
| `get_zestimate` | 1 | Just the Zestimate, rent Zestimate, tax assessed value, last sold price |
| `search_listings` | 1 per result | For sale, for rent or sold listings by location or bbox plus filters |
| `get_price_history` | 1 | List price changes, sale prices, withdrawals |
| `get_property_photos` | 1 | Photo gallery (responsive image URLs) |
| `get_property_schools` | 1 | Assigned schools with GreatSchools ratings |
| `get_listing_agent` | 1 | Listing agent and broker contact for an active listing |

Pick the narrowest tool: `get_zestimate` for a valuation question beats fetching the full record. The full record returns 250+ fields, so prefer the sub-resource tools when the user wants one slice.

Parameter details and response field notes: see [reference.md](reference.md).

## Authentication

Set `ZILLAPI_KEY` to your Zillapi API key (format `zk_...`).

```bash
export ZILLAPI_KEY="zk_..."
```

Free key at <https://zillapi.com/signup>: 100 credits, no card required. Plans and current prices: <https://zillapi.com/pricing/>. Failed calls are not charged.

## Errors

Every function returns a Python dict, never raises:

- `{"error": "auth", ...}`: `ZILLAPI_KEY` missing or invalid
- `{"error": "HTTP 404", ...}`: property not found
- `{"error": "HTTP 422", ...}`: bad parameter values
- `{"error": "HTTP 429", ...}`: rate limited, back off and retry
- `{"error": "network", ...}`: DNS or connection failure

## Reference

- Tool parameters and response notes: [reference.md](reference.md)
- OpenAPI spec: <https://zillapi.com/openapi.json>
- REST docs: <https://zillapi.com/api/properties/>
- Hosted MCP server (alternative to this skill): <https://api.zillapi.com/mcp>

## Trademark

Zillapi is an independent service and is not affiliated with, endorsed by, or sponsored by Zillow Group, Inc. "Zillow" and "Zestimate" are registered trademarks of Zillow Group, Inc.
