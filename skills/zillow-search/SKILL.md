---
name: zillow-search
version: 1.1.0
description: Searches US property listings for sale, for rent or sold via the zillapi API, filtered by location or bounding box, price, beds, baths, square footage, year built, home type and days on Zillow. Use when the user asks to find homes, condos, apartments, rentals, sold comparables or listings matching criteria in a city, ZIP or area. Do not use for a single known property (zillow-full covers lookups) or when a location appears incidentally. Each returned listing costs one credit, so keep max_items tight.
license: MIT-0
author: Zero Point Studio
homepage: https://zillapi.com
repository: https://github.com/ZeroPointRepo/zillow-skills
tags:
  - zillapi
  - zillow
  - real-estate
  - listings
  - search
  - property-data
  - api
metadata:
  openclaw:
    primaryEnv: ZILLAPI_KEY
    homepage: https://zillapi.com
    requires:
      env:
        - ZILLAPI_KEY
---

# zillow-search

Listing-search skill. Fire only on an explicit search request. Credits scale with results (1 per listing returned), so narrow filters and cap `max_items` before calling; confirm with the user when a query looks broad.

For one known property use [zillow-full](https://github.com/ZeroPointRepo/zillow-skills/tree/main/skills/zillow-full)'s `lookup_property_by_address` instead.

## Tool

### `search_listings` (1 credit per result, up to 50)

Pass either `location` or `bbox` (at least one required):

- `location`: city, ZIP or neighborhood string (`"Austin, TX"`, `"78704"`, `"Brooklyn, NY"`)
- `bbox`: `"west,south,east,north"` in decimal degrees

Filters:

- `status`: `for_sale` | `for_rent` | `sold` (default `for_sale`)
- `price_min`, `price_max`: integer dollars
- `beds_min`, `beds_max`, `baths_min`, `baths_max`: integers
- `sqft_min`, `sqft_max`, `year_built_min`, `year_built_max`: integers
- `home_types`: comma-separated subset of `house`, `condo`, `townhouse`, `multi_family`, `manufactured`, `lot`, `apartment`
- `days_on_zillow`: one of `"1"`, `"7"`, `"14"`, `"30"`, `"90"`, `"6m"`, `"12m"`, `"24m"`, `"36m"`
- `max_items`: integer, capped at 50 per call

A search returning 25 results consumes 25 credits.

## Authentication

Set `ZILLAPI_KEY` to your Zillapi API key (format `zk_...`).

```bash
export ZILLAPI_KEY="zk_..."
```

Free key at <https://zillapi.com/signup>: 100 credits, no card required. Plans and current prices: <https://zillapi.com/pricing/>. Failed calls are not charged.

## Errors

The handler returns dicts, never raises:

- `{"error": "auth", ...}`: `ZILLAPI_KEY` missing or invalid
- `{"error": "HTTP 422", ...}`: bad filter values, check the parameter list above
- `{"error": "HTTP 429", ...}`: rate limited, back off and retry
- `{"error": "network", ...}`: DNS or connection failure

## Reference

- OpenAPI spec: <https://zillapi.com/openapi.json>
- REST docs: <https://zillapi.com/api/properties/>
- Hosted MCP server (alternative to this skill): <https://api.zillapi.com/mcp>

## Trademark

Zillapi is an independent service and is not affiliated with, endorsed by, or sponsored by Zillow Group, Inc. "Zillow" is a registered trademark of Zillow Group, Inc.
