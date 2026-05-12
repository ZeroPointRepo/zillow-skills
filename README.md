# zillow-skills

Agent skills for U.S. property data via [Zillapi.com](https://zillapi.com).

Three drop-in skills that let agents look up Zillow property data — Zestimates, listings, photos, schools, taxes, price history, agent contact — over the Zillapi REST API. Pure Python standard library, no dependencies, MIT-0 licensed.

## Install

```bash
# OpenClaw (via ClawHub)
npx clawhub@latest install zillow-full

# Hermes Agent
hermes skills install skills-sh/nikhonit/zillow-skills/skills/zillow-full

# Generic agent skills (Claude Code, Cursor, Cline)
npx skills add nikhonit/zillow-skills
```

## Skills in this repo

| Skill | Purpose | Cost |
|---|---|---|
| [`zillow-full`](skills/zillow-full) | Complete property data toolkit — address lookup, URL lookup, Zestimate, search, history, photos, schools, agent | 1 credit per call |
| [`zillow-zestimate`](skills/zillow-zestimate) | Zestimate-only valuation lookups (lighter response) | 1 credit per call |
| [`zillow-search`](skills/zillow-search) | Bounding-box and location-based listing search | 1 credit per listing returned |

Install the bundled `zillow-full` for agents that need broad coverage. Install the focused variants when you want minimum tool surface.

## Authentication

Set the `ZILLAPI_KEY` environment variable to your Zillapi API key (format `zk_...`).

```bash
export ZILLAPI_KEY="zk_..."
```

Get a free key with 100 credits at [zillapi.com/signup](https://zillapi.com/signup) — no card required.

## Pricing

| Plan | Price | Credits | Rate limit | Top-ups |
|---|---|---|---|---|
| Free | $0 | 100 (one-time) | 20/min | not available |
| Monthly | $5/mo | 1,000/month | 200/min | $4 per 1,000 |
| Annual | $54/yr | 12,000 upfront | 300/min | $3 per 1,000 |

One credit equals one property record returned. Failed calls do not consume credits.

## Source

- API reference: <https://zillapi.com/openapi.json>
- Hosted MCP server: <https://api.zillapi.com/mcp>
- Quickstart: <https://zillapi.com/quickstart/>

## Issues and contributions

See [CONTRIBUTING.md](CONTRIBUTING.md). Security reports: [SECURITY.md](SECURITY.md).

## License

[MIT No Attribution](LICENSE). Fork, ship, sublicense — no attribution required.

## Trademark

Zillapi is an independent service and is not affiliated with, endorsed by, or sponsored by Zillow Group, Inc. "Zillow" and "Zestimate" are registered trademarks of Zillow Group, Inc.
