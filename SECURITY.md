# Security policy

## Reporting a vulnerability

Email **nikhil@landkit.pro** with the subject line `SECURITY: zillow-skills`. Please do not open public issues for security reports.

We will acknowledge receipt within 72 hours and aim to publish a fix or mitigation within 14 days for confirmed issues.

## Dependency surface

The handlers in this repository use only the Python standard library:

- `urllib.request`, `urllib.parse`, `urllib.error` — HTTPS calls to `api.zillapi.com`
- `json` — request/response serialization
- `os` — reading the `ZILLAPI_KEY` environment variable

There are no third-party packages, no transitive dependencies, and no build step. The only network destination is `https://api.zillapi.com`.

## Credential handling

The skills read the API key from the `ZILLAPI_KEY` environment variable at call time. They do not cache the key, write it to disk, or log it. Failed requests return a structured error rather than raising, so the key cannot leak into a traceback.

## Trademark

Zillapi is an independent service and is not affiliated with, endorsed by, or sponsored by Zillow Group, Inc.
