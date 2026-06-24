# MEMORY.md

Session reference for the Portfolio-website project. Covers work done across Claude Code sessions (May–June 2025). Use this to orient a new session without re-deriving history.

---

## What has been built / changed

### June 2025 session (most recent)

| Change | Files touched |
|---|---|
| Venture names in journey timeline are invisible hyperlinks to venture pages | `journey.html` |
| All `<p>` text is justified sitewide | All 6 HTML files |
| Em-dashes (`—`) replaced with `, ` sitewide | All 6 HTML files |
| Real portrait photo (`pulkit.jpg`) added to index hero | `index.html` |
| Solar farm cover image added to Pujan Energy page | `pujan-energy.html` |
| Animated footprints + side-profile portrait circle added to journey hero | `journey.html` |
| Memoji favicon created (with face zoom-in fix) | `favicon.ico`, `favicon-32x32.png`, `apple-touch-icon.png` |
| Lenskart store collage (4-panel, warm color-graded) added | `lenskart.html`, `lenskart-store.jpg` |
| CLAUDE.md updated with favicon + Radhe Radhe mandatory requirements | `CLAUDE.md` |
| Journey timeline reversed to chronological order (oldest first) | `journey.html` |
| Security audit + fixes: CSP, Referrer-Policy, Permissions-Policy on all pages | All 6 HTML files |
| `.gitignore` created | `.gitignore` |
| Contact email HTML-entity obfuscated | `index.html` |

---

## Known issues / limitations

| Issue | Severity | Status |
|---|---|---|
| `pulkit.jpg` is 6.1 MB (full DSLR) in the public repo | Low | Open — needs a resized version committed and the `<img>` pointed to it |
| `Pulkit.jpg` (capital P) is also tracked in git history alongside `pulkit.jpg` | Low | Open — removing requires git history rewrite (force push); not urgent |
| `CLAUDE.md` and `AGENTS.md` are public in the repo | Low | Accepted — they contain no secrets |
| `X-Frame-Options` / `frame-ancestors` need HTTP headers, not meta tags | Low | Open — add `_headers` file if hosting on Netlify/Vercel |
| Google Fonts loaded without Subresource Integrity (SRI) | Info | Open — low risk, but could add `integrity=` attribute for hardening |

---

## Image processing recipes

### Cover image (1920×928px, warm-graded)
```python
from PIL import Image, ImageEnhance
img = Image.open("source.jpg").convert("RGB")
# Cover-crop to 1920×928
scale = max(1920/img.width, 928/img.height)
img = img.resize((int(img.width*scale), int(img.height*scale)), Image.LANCZOS)
left = (img.width - 1920) // 2
top = (img.height - 928) // 2
img = img.crop((left, top, left+1920, top+928))
# Color grade
img = ImageEnhance.Color(img).enhance(0.82)
img = ImageEnhance.Brightness(img).enhance(0.93)
warm = Image.new("RGB", img.size, (175, 128, 88))  # #af8058
img = Image.blend(img, warm, 0.10)
img.save("output.jpg", quality=88)
```

### Portrait circle (500×500px, face-focused)
```python
from PIL import Image
img = Image.open("source.jpg").convert("RGB")
# Square crop — pick center-top area
size = min(img.width, img.height)
left = (img.width - size) // 2
img = img.crop((left, 0, left + size, size))
img = img.resize((500, 500), Image.LANCZOS)
img.save("pulkit-right.jpg", quality=88)
```

### Favicon (from memoji PNG, auto-centered)
```python
from PIL import Image
img = Image.open("memoji.png").convert("RGBA")
bbox = img.getbbox()
cropped = img.crop(bbox)
# Add padding and make square
size = max(cropped.width, cropped.height) + 16
canvas = Image.new("RGBA", (size, size), (0,0,0,0))
x = (size - cropped.width) // 2
y = (size - cropped.height) // 2
canvas.paste(cropped, (x, y))
canvas.resize((32, 32), Image.LANCZOS).save("favicon-32x32.png")
canvas.resize((180, 180), Image.LANCZOS).save("apple-touch-icon.png")
# ICO with multiple sizes
ico_img = canvas.resize((48, 48), Image.LANCZOS)
ico_img.save("favicon.ico", format="ICO", sizes=[(16,16),(32,32),(48,48)])
```

---

## Animation: footprints (journey.html hero)

The SVG footprint trail uses **opacity-only** animation (`fp-loop` keyframe). Do NOT use `transform` or `transform-origin` inside `@keyframes` — browsers silently ignore the entire animation if those appear there.

Negative `animation-delay` values are required for infinite loops. With `animation: name duration infinite`, delay only affects the first iteration. To phase-offset k footprints across a T-second cycle: `delay = -(T - k * step)s`.

---

## Git workflow note

Codex also commits and pushes to this same repo (`origin/main`). Before making changes in a new session, always run:
```
git pull origin main
```
to avoid push rejections from a diverged branch.

---

## Potential next work items

These were mentioned or implied but not yet done:

- Add a new venture page (same template as existing case studies)
- Resize `pulkit.jpg` to a web-optimised version (~400–600KB) and commit that instead
- Add Netlify `_headers` file for proper `X-Frame-Options` and `frame-ancestors` HTTP headers
- Consider SRI hashes for the Google Fonts `<link>` tag
- Mobile review of the journey page hero (footprints + portrait are hidden on `max-width: 768px`)
