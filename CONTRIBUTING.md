# Contributing

Pull requests welcome for:

- New skills exposing additional Zillapi endpoints
- Bug fixes in existing handlers
- Additional language ports (Node, Go, Rust)
- Documentation improvements

## Ground rules

- Skills must remain dependency-free. Use only the Python standard library (`urllib`, `json`, `os`).
- Each skill must pass `python -m unittest discover` from its `tests/` directory before submission.
- Never commit credentials. The `ZILLAPI_KEY` environment variable is the only auth surface.
- Sign-off your commits (`git commit -s`).
- Match the existing handler error contract: return `{"error": "<code>", "detail": "<message>"}` instead of raising.

## Local development

```bash
git clone https://github.com/nikhonit/zillow-skills.git
cd zillow-skills/skills/zillow-full
ZILLAPI_KEY=zk_... python3 -m unittest discover tests
```

## License

By contributing you agree that your contributions are licensed under the [MIT No Attribution](LICENSE) license.
