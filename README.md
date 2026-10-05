# Pulkit Viradiya portfolio

Static, self-contained HTML portfolio for [pulkitviradiya.in](https://www.pulkitviradiya.in/).

```sh
python3 concept-build.py --production
python3 -m http.server 8080
```

Open `http://localhost:8080/` to review the production pages. Run
`python3 concept-build.py` without flags to regenerate local `concept-*.html`
previews. See `AGENTS.md` and `docs/architecture.md` for the page map and
release notes.
