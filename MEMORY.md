# MEMORY.md

## Project state
- Site is 6 standalone static HTML files, no build step, no framework. Repo: `github.com/pulkitviradiya/Portfolio-website`.
- Codex also pushes to `origin/main` — always `git pull origin main` before editing.

## Known issues
- `pulkit.jpg` (6.1 MB DSLR original) is unoptimised in the public repo; should be replaced with a ~500 KB resized version.
- `Pulkit.jpg` (capital P) is also tracked in git history alongside `pulkit.jpg`; removing it requires a force-push history rewrite, accepted as low-priority for now.
- `X-Frame-Options` / `frame-ancestors` require HTTP response headers — the meta tags added are insufficient; add a `_headers` file when deploying to Netlify/Vercel.
- Google Fonts are loaded without SRI hashes; low risk but noted as a future hardening opportunity.

## Next work items
- Resize `pulkit.jpg` to ~500 KB and update the `<img>` reference in `index.html`.
- Add Netlify/Vercel `_headers` file for proper clickjacking protection.
- Mobile review: journey hero footprints + portrait circle are hidden at `max-width: 768px` — confirm this is intentional.
- Add a new venture page when needed by copying an existing case study and following CLAUDE.md mandatory requirements.

## Image specs (quick reference)
- Cover images: 1920×928 px JPEG, PIL Color 0.82 / Brightness 0.93 / warm overlay `#af8058` at alpha 0.10.
- Portrait circle: 500×500 px JPEG, square-cropped from top-center of source image.
- Favicon: auto-detect content bbox, add 8 px padding, export 16/32/48 px ICO + 32 px PNG + 180 px PNG.
