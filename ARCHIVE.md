# ARCHIVE.md

Reference-only. Do not read at session start. Pull this up only when asked about historical context.

---

## [2025-06-25] June 2025 session — change log

| Change | Files touched |
|---|---|
| Venture names in journey timeline made invisible hyperlinks to venture pages | `journey.html` |
| All `<p>` text justified sitewide | All 6 HTML files |
| Em-dashes replaced with `, ` sitewide | All 6 HTML files |
| Real portrait photo (`pulkit.jpg`) added to index hero | `index.html` |
| Solar farm cover image added to Pujan Energy page | `pujan-energy.html` |
| Animated footprints + side-profile portrait circle added to journey hero | `journey.html` |
| Memoji favicon created (face zoom-in fix applied) | `favicon.ico`, `favicon-32x32.png`, `apple-touch-icon.png` |
| Lenskart store collage (4-panel, warm color-graded) added | `lenskart.html`, `lenskart-store.jpg` |
| Journey timeline reversed to chronological order (oldest first) | `journey.html` |
| Security audit + fixes: CSP, Referrer-Policy, Permissions-Policy on all pages | All 6 HTML files |
| `.gitignore` created | `.gitignore` |
| Contact email HTML-entity obfuscated | `index.html` |
| `CLAUDE.md`, `AGENTS.md`, `MEMORY.md`, `ARCHIVE.md` created/updated | Documentation |

---

## [2025-06-25] Image processing recipes (full code)

### Cover image — 1920×928 px, warm-graded
```python
from PIL import Image, ImageEnhance
img = Image.open("source.jpg").convert("RGB")
scale = max(1920/img.width, 928/img.height)
img = img.resize((int(img.width*scale), int(img.height*scale)), Image.LANCZOS)
left = (img.width - 1920) // 2
top = (img.height - 928) // 2
img = img.crop((left, top, left+1920, top+928))
img = ImageEnhance.Color(img).enhance(0.82)
img = ImageEnhance.Brightness(img).enhance(0.93)
warm = Image.new("RGB", img.size, (175, 128, 88))  # #af8058
img = Image.blend(img, warm, 0.10)
img.save("output.jpg", quality=88)
```

### Portrait circle — 500×500 px, face-focused
```python
from PIL import Image
img = Image.open("source.jpg").convert("RGB")
size = min(img.width, img.height)
left = (img.width - size) // 2
img = img.crop((left, 0, left + size, size))
img = img.resize((500, 500), Image.LANCZOS)
img.save("pulkit-right.jpg", quality=88)
```

### Favicon — from memoji PNG, auto-centered
```python
from PIL import Image
img = Image.open("memoji.png").convert("RGBA")
bbox = img.getbbox()
cropped = img.crop(bbox)
size = max(cropped.width, cropped.height) + 16
canvas = Image.new("RGBA", (size, size), (0,0,0,0))
x = (size - cropped.width) // 2
y = (size - cropped.height) // 2
canvas.paste(cropped, (x, y))
canvas.resize((32, 32), Image.LANCZOS).save("favicon-32x32.png")
canvas.resize((180, 180), Image.LANCZOS).save("apple-touch-icon.png")
ico_img = canvas.resize((48, 48), Image.LANCZOS)
ico_img.save("favicon.ico", format="ICO", sizes=[(16,16),(32,32),(48,48)])
```

---

## [2025-06-25] Animation notes — footprints (journey.html)

The SVG footprint trail uses opacity-only animation (`fp-loop` keyframe). Using `transform` or `transform-origin` inside `@keyframes` causes browsers to silently ignore the entire animation.

Negative `animation-delay` bakes phase offsets into infinite loops — for k footprints across a T-second cycle: `delay = -(T - k * step)s`.
