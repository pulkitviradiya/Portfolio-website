# Tasks

## Current Sprint

*(Fill in manually)*

---

## Open issues

| Priority | Task | Detail |
|---|---|---|
| Medium | Resize `pulkit.jpg` | 6.1 MB DSLR original is in the public repo; replace with ~500 KB version and update `<img>` in `index.html` |
| Low | Add `_headers` file | `X-Frame-Options` and `frame-ancestors` need HTTP headers for full clickjacking protection; add `_headers` (Netlify) or `netlify.toml` / `vercel.json` when deploying |
| Low | Mobile review — journey hero | Footprints + portrait circle are hidden at `max-width: 768px` via `display: none` on `.j-deco`; confirm this is intentional or add a mobile fallback |
| Low | Google Fonts SRI | Fonts loaded without `integrity=` hashes; low risk but a future hardening option |
| Low | Remove `Pulkit.jpg` from git history | Capital-P duplicate is tracked alongside `pulkit.jpg`; removing requires `git filter-branch` or `git-filter-repo` + force push |

---

## TODO comments in code

None found as of 2026-06-25 scan.

---

## Completed (archived)

See [ARCHIVE.md](../ARCHIVE.md) for the full June 2026 session change log.
