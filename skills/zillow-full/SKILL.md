---
name: zillow-full
version: 1.0.1
description: Complete Zillow property data toolkit via Zillapi.com. Nine tools — address/URL/zpid lookup, Zestimate, listings search, photos, schools, price history, agent contact.
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
metadata:
  openclaw:
    primaryEnv: ZILLAPI_KEY
    homepage: https://zillapi.com
    requires:
      env:
        - ZILLAPI_KEY
---

# zillow-full

Complete Zillow property data toolkit via Zillapi.com. Use when the user **explicitly asks** about a U.S. property, its value, listings to buy or rent, or related real-estate data.

## When to use this skill

Each tool call consumes Zillapi credits, so this skill activates only when the user's request is genuinely about real-estate data — not when an address or Zillow link merely appears in passing.

**DO use when the user:**

- Asks about a Zestimate, property value, rent estimate, or tax-assessed value → `get_zestimate`
- Pastes a Zillow URL and asks about that property → `lookup_property_by_url`
- Gives an address and asks about the property, schools, photos, or agent → `lookup_property_by_address`
- Asks to find homes matching criteria (location, price range, beds, baths) → `search_listings`
- Asks for the price history, last sale, or ownership timeline of a known property → `get_price_history`
- Asks for the listing agent or broker contact → `get_listing_agent`
- Asks what schools serve a property → `get_property_schools`
- Asks to see photos of a property → `get_property_photos`

**Do NOT use when:**

- An address appears incidentally in context (email signatures, news articles, copy-pasted unrelated content)
- The user is discussing real estate abstractly without asking for data on a specific property or listing search
- The user has not signaled they want a property lookup

When the intent is ambiguous, ask the user to confirm before calling a tool. These tools cost credits and return large records the user may not want.

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
