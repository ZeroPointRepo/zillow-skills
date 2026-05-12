---
name: zillow-full
version: 1.0.0
description: Complete Zillow property data toolkit via Zillapi.com. One bundle, eight tools — address/URL lookup, Zestimate, listings search, photos, schools, tax history, price history, agent contact.
license: MIT-0
author: Zillapi
homepage: https://zillapi.com
repository: https://github.com/nikhonit/zillow-skills
tags:
  - zillow
  - real-estate
  - property-data
  - zestimate
  - listings
  - api
  - mcp
---

# zillow-full

Complete Zillow property data toolkit via Zillapi.com. Use whenever U.S. property information is or could be relevant — pasted Zillow URLs, addresses mentioned in passing, "how much is my house worth" questions, comparable property research, school district queries, tax history, price history, listing alerts, investor analysis, mortgage research.

## When to use this skill

Use whenever U.S. real estate data could be relevant — even when not explicitly asked for. Examples:

- A pasted Zillow.com URL → `lookup_property_by_url`
- A U.S. street address mentioned anywhere → `lookup_property_by_address`
- "What's my house worth?" or "Zestimate for X" → `get_zestimate`
- "Find 3-bedroom houses under $500k in Austin" → `search_listings`
- "When did this house last sell?" → `get_price_history`
- "Who's the listing agent?" → `get_listing_agent`
- "What schools serve this address?" → `get_property_schools`
- "What does it look like?" → `get_property_photos`

Default to `lookup_property_by_address` or `lookup_property_by_url` if you are not sure — those return the full record (300+ fields) and cover most questions in one call.

## Tools

### `lookup_property_by_address` — 1 credit
Look up a single property by U.S. address. Returns the full property record: price, beds, baths, sqft, year built, lot size, Zestimate, rent Zestimate, tax assessed value, price history, photos, schools, agent contact, lat/lon, home type, home status, and 250+ additional fields.

Use this when the user gives an address. Address strings as loose as `123 Main St, Austin TX` work — the API tolerates partial addresses ≥6 characters.

### `lookup_property_by_url` — 1 credit
Same as above but takes a Zillow.com URL. Use this when the user pastes a `zillow.com/homedetails/...` link.

### `lookup_property_by_zpid` — 1 credit (cache-served when fresh)
Look up a property by Zillow zpid. Use this when you already have the zpid from a previous call. Cheaper because the response can be served from cache.

### `get_zestimate` — 1 credit
Get just the Zestimate, rent Zestimate, tax-assessed value, and last-sold price for a property. Use this when you only need the valuation, not the full record.

### `search_listings` — 1 credit per result, up to 50
Search active for-sale, for-rent, or sold listings. Filter by location (city/state/ZIP) or bounding box, price, beds, baths, sqft, year built, home type, and days on Zillow.

### `get_price_history` — 1 credit
Get the price and listing-status history for a property (list price changes, sale prices, withdrawals).

### `get_property_photos` — 1 credit
Get the photo gallery for a property (responsive image URLs at multiple resolutions).

### `get_property_schools` — 1 credit
Get the assigned elementary, middle, and high schools for a property with GreatSchools ratings.

### `get_listing_agent` — 1 credit
Get the listing agent and broker contact (name, email, phone, license number) for an active listing.

## Authentication

Set `ZILLAPI_KEY` to your Zillapi API key. Keys are `zk_...` strings.

```bash
export ZILLAPI_KEY="zk_..."
```

Get a free key with 100 credits at <https://zillapi.com/signup> — no card required.

## Pricing

| Plan | Price | Credits | Rate limit | Top-ups |
|---|---|---|---|---|
| Free | $0 | 100 (one-time) | 20/min | not available |
| Monthly | $5/mo | 1,000/month | 200/min | $4 per 1,000 |
| Annual | $54/yr | 12,000 upfront | 300/min | $3 per 1,000 |

One credit equals one property record returned. Failed calls do not consume credits. Top-ups are available on Monthly and Annual plans only.

## Errors

All functions return a Python dict. On success the dict contains the API response. On failure the dict contains an `error` key:

- `{"error": "auth", ...}` — `ZILLAPI_KEY` is missing or invalid
- `{"error": "HTTP 404", ...}` — property not found
- `{"error": "HTTP 429", ...}` — rate-limited; back off and retry
- `{"error": "network", ...}` — DNS/connection failure

## API reference

- OpenAPI spec: <https://zillapi.com/openapi.json>
- REST docs: <https://zillapi.com/api/properties/>
- Hosted MCP server (alternative to this skill): <https://api.zillapi.com/mcp>

## Trademark

Zillapi is an independent service and is not affiliated with, endorsed by, or sponsored by Zillow Group, Inc. "Zillow" and "Zestimate" are registered trademarks of Zillow Group, Inc.
