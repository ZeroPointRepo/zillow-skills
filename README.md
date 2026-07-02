# zillow-skills

**Agent skills for U.S. Zillow property data.** Three drop-in skills that let any agent look up Zestimates, listings, photos, schools, taxes, price history, and agent contact over the [Zillapi REST API](https://zillapi.com).

Free to use — [grab a key](https://zillapi.com/signup) (100 credits, no card required) and you're calling Zillow data from Claude, ChatGPT, Cursor, or your own agent loop in under two minutes.

Pure Python standard library. No dependencies. MIT-0 licensed.

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

**[Get a free key in 30 seconds](https://zillapi.com/signup)** — 100 credits, no card required. The same key works for these skills, the [hosted MCP server](https://api.zillapi.com/mcp), and direct REST calls.

## Pricing

Free tier: 100 credits at signup — no credit card, 20 requests/minute. One credit equals one property record returned. Failed calls do not consume credits. Full pricing: [zillapi.com/pricing](https://zillapi.com/pricing).

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
