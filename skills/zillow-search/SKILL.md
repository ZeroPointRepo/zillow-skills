---
name: zillow-search
version: 1.0.0
description: Search U.S. property listings by location or bounding box, price, beds, and home type via Zillapi.com.
license: MIT-0
author: Zillapi
homepage: https://zillapi.com
repository: https://github.com/nikhonit/zillow-skills
tags:
  - zillow
  - real-estate
  - listings
  - search
  - api
  - mcp
---

# zillow-search

Focused listing-search skill. Use whenever the user wants to find homes matching a set of criteria — not look up one specific property.

## When to use this skill

- "Find 3-bedroom houses under $500k in Austin, TX"
- "What's for rent under $2,500 in 78704?"
- "Show me sold comparables for this neighborhood in the last 90 days"
- "Search for waterfront condos in Miami"

For looking up one known property, use [`zillow-full`](https://github.com/nikhonit/zillow-skills/tree/main/skills/zillow-full) — `lookup_property_by_address` or `lookup_property_by_url`.

## Tools

### `search_listings` — 1 credit per result, up to 50

Search active for-sale, for-rent, or sold listings.

Filters:

- `location` — city, ZIP, neighborhood string (e.g. `"Austin, TX"`, `"78704"`, `"Brooklyn, NY"`)
- `bbox` — `"west,south,east,north"` decimal degrees (alternative to location)
- `status` — `for_sale` | `for_rent` | `sold` (default `for_sale`)
- `price_min`, `price_max` — integer dollars
- `beds_min`, `beds_max`, `baths_min`, `baths_max` — integers
- `sqft_min`, `sqft_max`, `year_built_min`, `year_built_max` — integers
- `home_types` — comma-separated subset of: `house`, `condo`, `townhouse`, `multi_family`, `manufactured`, `lot`, `apartment`
- `days_on_zillow` — one of `"1"`, `"7"`, `"14"`, `"30"`, `"90"`, `"6m"`, `"12m"`, `"24m"`, `"36m"`
- `max_items` — integer, capped at 50 per call

Pass either `location` or `bbox` — at least one is required.

## Authentication

Set `ZILLAPI_KEY` to your Zillapi API key (format `zk_...`). Free key with 100 credits at <https://zillapi.com/signup> — no card.

## Pricing

| Plan | Price | Credits | Rate limit | Top-ups |
|---|---|---|---|---|
| Free | $0 | 100 (one-time) | 20/min | not available |
| Monthly | $5/mo | 1,000/month | 200/min | $4 per 1,000 |
| Annual | $54/yr | 12,000 upfront | 300/min | $3 per 1,000 |

One credit per listing returned. A search returning 25 results consumes 25 credits.

## Trademark

Zillapi is an independent service and is not affiliated with, endorsed by, or sponsored by Zillow Group, Inc. "Zillow" is a registered trademark of Zillow Group, Inc.
