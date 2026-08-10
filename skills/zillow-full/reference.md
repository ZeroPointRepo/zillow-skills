# zillow-full tool reference

Parameter details and response notes for every tool in this skill. All facts match handler.py signatures and the live OpenAPI spec at https://zillapi.com/openapi.json.

## Contents

- Lookup tools (by address, by URL, by zpid)
- get_zestimate
- search_listings
- Sub-resource tools (price history, photos, schools, agent)
- Shared conventions (zpid resolution, field projection, credits)

## Lookup tools

### `lookup_property_by_address(address, status="FOR_SALE", fields=None)`

- `address`: street address string, minimum 6 characters. Loose strings work (`"123 Main St, Austin TX"`).
- `status`: `FOR_SALE` | `RECENTLY_SOLD` | `FOR_RENT` (default `FOR_SALE`). Lookup statuses are uppercase; search statuses are lowercase (see search_listings).
- `fields`: optional comma-separated dotted-path projection, e.g. `"zpid,price,zestimate,address.streetAddress"`. Use it to shrink the 250+ field record to the slice you need.

### `lookup_property_by_url(url, status="FOR_SALE", extract_units="disabled", fields=None)`

- `url`: a `zillow.com/homedetails/...` link the user pasted.
- `extract_units`: `disabled` | `all` | `for_sale` | `for_rent` | `recently_sold` | `off_market`. Use `all` when the URL points at a multi-unit building and the user wants the unit list.

### `lookup_property_by_zpid(zpid, fields=None)`

- Cheapest lookup: cache-served when fresh. Prefer it whenever a previous call already returned the zpid.

## `get_zestimate(zpid=None, address=None)`

- Pass `zpid` when known (skips the address-resolution call). With only `address`, the handler first resolves the zpid (that resolution is itself a lookup call), then hits the dedicated zestimate endpoint.
- Returns `zestimate`, `rent_zestimate`, `tax_assessed_value`, `last_sold_price`, `currency`.

## `search_listings(...)`

- Location: pass either `location` (city, ZIP or neighborhood string) or `bbox` (`"west,south,east,north"` decimal degrees). At least one is required.
- `status`: `for_sale` | `for_rent` | `sold` (lowercase, default `for_sale`).
- Numeric filters: `price_min`, `price_max`, `beds_min`, `beds_max`, `baths_min`, `baths_max`, `sqft_min`, `sqft_max`, `year_built_min`, `year_built_max` (integers).
- `home_types`: comma-separated subset of `house`, `condo`, `townhouse`, `multi_family`, `manufactured`, `lot`, `apartment`.
- `days_on_zillow`: one of `"1"`, `"7"`, `"14"`, `"30"`, `"90"`, `"6m"`, `"12m"`, `"24m"`, `"36m"` (string).
- `max_items`: capped at 50 per call. Credits equal results returned: a 25-result search costs 25 credits, so keep this tight.

## Sub-resource tools

`get_price_history`, `get_property_photos`, `get_property_schools`, `get_listing_agent` all take `(zpid=None, address=None)`:

- Prefer `zpid`. With only `address`, the handler resolves the zpid first (one extra lookup call).
- `get_price_history`: list price changes, sale prices, withdrawals with dates.
- `get_property_photos`: responsive image URLs at multiple resolutions.
- `get_property_schools`: assigned elementary, middle and high schools with GreatSchools ratings.
- `get_listing_agent`: agent and broker name, email, phone and license number for an active listing.

## Shared conventions

- Every function returns a dict. Success: the API response under `data`. Failure: an `error` key (`auth`, `not_found`, `invalid_argument`, `network`, `unexpected`, or `HTTP <code>` with `detail`).
- Handlers are pure Python standard library, no dependencies to install.
- One credit per record returned on success; failed calls (4xx, 5xx) and rate-limited calls (429) are never charged. Current plans and prices: https://zillapi.com/pricing/
