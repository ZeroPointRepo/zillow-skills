---
name: zillow-zestimate
version: 1.0.1
description: Zillow Zestimate (property valuation) and rent Zestimate lookups via Zillapi.com. One tool, minimum surface area.
license: MIT-0
author: Zillapi
homepage: https://zillapi.com
repository: https://github.com/nikhonit/zillow-skills
tags:
  - zillow
  - zestimate
  - real-estate
  - valuation
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

# zillow-zestimate

Focused valuation skill. Use only when the user **explicitly asks** for a property value — the Zestimate, rent Zestimate, tax-assessed value, or last sale price.

## When to use this skill

**DO use when the user asks:**

- "What's the Zestimate on 123 Main St?"
- "How much is my house worth?"
- "What's the rental Zestimate?"
- "What did this house last sell for?"
- "What's the tax-assessed value?"

**Do NOT use when:**

- An address appears incidentally in context (email signatures, unrelated documents)
- The user mentions a property without asking for its value
- The user has not signaled they want a valuation lookup

If you also need photos, schools, agent contact, or price history, use [`zillow-full`](https://github.com/nikhonit/zillow-skills/tree/main/skills/zillow-full) instead — it bundles everything in one install.

## Tools

### `get_zestimate` — 1 credit

Returns:

```json
{
  "data": {
    "zestimate": 489500,
    "rent_zestimate": 2800,
    "tax_assessed_value": 410000,
    "last_sold_price": 375000,
    "currency": "USD"
  }
}
```

Pass either `zpid` (preferred — cheaper) or `address`. If only `address` is given, the handler resolves the zpid first.

## Authentication

Set `ZILLAPI_KEY` to your Zillapi API key (format `zk_...`). Free key with 100 credits at <https://zillapi.com/signup> — no card.

## Pricing

| Plan | Price | Credits | Rate limit | Top-ups |
|---|---|---|---|---|
| Free | $0 | 100 (one-time) | 20/min | not available |
| Monthly | $5/mo | 1,000/month | 200/min | $4 per 1,000 |
| Annual | $54/yr | 12,000 upfront | 300/min | $3 per 1,000 |

## Trademark

Zillapi is an independent service and is not affiliated with, endorsed by, or sponsored by Zillow Group, Inc. "Zillow" and "Zestimate" are registered trademarks of Zillow Group, Inc.
