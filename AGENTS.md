# CLAUDE.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

---

## Session & memory management

At the start of every session, read `MEMORY.md` before responding. Use what you find to inform your work. Don't announce what you found, just be informed by it.

When Pulkit says "remember this," write the information to `MEMORY.md` immediately and confirm you've done it.

### Where things go

Apply two tests when deciding where to save something:

- **Test 1 — behaviour?** Look for words like "always," "never," "before doing X, do Y." If yes, add it to this file (`CLAUDE.md`) under the appropriate section.
- **Test 2 — fact about the world?** Contact details, project status, decisions, things Pulkit has said to remember. If yes, add it to `MEMORY.md`. When unsure, suggest which file you think it belongs in and ask for confirmation.

### Dates

Always double-check the current year before writing any date. The current date is available in the system context — never assume or hardcode a year.

### Git workflow

Codex also pushes to `origin/main`. Always run `git pull origin main` before making any changes in a new session to avoid push rejections.

### Memory hygiene rules

1. Keep each `MEMORY.md` entry to two sentences max.
2. Keep root `MEMORY.md` under 150 lines; if it exceeds 150, compress verbose entries first, then archive the overflow to `ARCHIVE.md`.
3. Current-state content (active projects, contact info, working conventions) stays in `MEMORY.md` regardless of age.
4. When a project completes or an entry becomes outdated, move it from `MEMORY.md` to `ARCHIVE.md` automatically.
5. `ARCHIVE.md` is reference-only: never read at session start, only pulled up when asked about something historical.

---

## Overview

Static personal portfolio website for Pulkit Viradiya — no build step, no framework, no dependencies. Open any `.html` file directly in a browser to preview it.

To serve locally with live reload:
```
python3 -m http.server 8080
# or
npx serve .
```

## Architecture

The site is **six standalone HTML files**, each fully self-contained: all CSS lives in a `<style>` block in `<head>`, and all JavaScript is in a `<script>` block at the bottom of `<body>`. There are no external JS libraries, no bundler, and no shared CSS/JS files.

| File | Role |
|---|---|
| `index.html` | Home / landing page — hero, about, ventures grid, contact |
| `journey.html` | Long-form narrative timeline of Pulkit's career |
| `candy-floss.html` | Case study — Candy Floss fashion brand |
| `lenskart.html` | Case study — Lenskart franchise chapter |
| `ximivogue.html` | Case study — Ximivogue brand |
| `pujan-energy.html` | Case study — Pujan Energy |

### Shared patterns (duplicated across all files)

Every page reproduces the same blocks verbatim — changes to nav, theme logic, or design tokens must be made in **each file individually**:

- **Design tokens** — CSS custom properties in `:root` (`--bg`, `--ink`, `--accent`, `--serif`, `--sans`, `--maxw`, `--pad`, `--section-pad`) and a `[data-theme="dark"]` override block.
- **Dark-mode toggle** — `<html data-theme="light|dark">` toggled by a button (`#themeToggle`); preference persisted in `localStorage('theme')`; respects `prefers-color-scheme` on first visit.
- **Full-screen nav overlay** — `.menu-overlay` toggled by `.menu-pill` button; closed on `Escape` or any `[data-menu-link]` click; sets `body.overflow = 'hidden'` while open.
- **Scroll-triggered nav** — `window.scroll` listener adds `.scrolled` class to `#nav` after 20 px, enabling the frosted-glass background.
- **Reveal animations** — `.reveal` elements use `IntersectionObserver` to add `.in`, triggering a CSS fade-up transition; stagger via `.delay-1` through `.delay-4`.
- **Marquee** — CSS `@keyframes marquee` infinite scroll on `.marquee-track`.

---

## Mandatory page requirements

Every new page **must** include all of the following — no exceptions.

### 1. Head structure order (in `<head>`)

```html
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; script-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'none'; base-uri 'self'; form-action 'none';">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta http-equiv="Permissions-Policy" content="camera=(), microphone=(), geolocation=(), payment=()">
<link rel="icon" type="image/x-icon" href="favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
```

Favicon files live at repo root: `favicon.ico`, `favicon-32x32.png`, `apple-touch-icon.png` (memoji, transparent background).

### 2. Radhe Radhe greeting (placed immediately above `<footer>`)

```html
<div class="radhe-section">
  <hr class="radhe-rule">
  <span class="radhe-text">|| राधे राधे ||</span>
  <hr class="radhe-rule">
</div>
```

Required CSS (copy into every page's `<style>` block):
```css
.radhe-section { text-align: center; padding: 2.5rem var(--pad) 2.5rem; }
.radhe-rule { border: none; height: 1px;
  background: linear-gradient(to right, transparent, #b5872a 30%, #b5872a 70%, transparent);
  margin: 0 auto; max-width: 420px; }
.radhe-text { font-family: var(--serif); font-size: 1.65rem; font-weight: 700;
  letter-spacing: 0.24em; color: #b5872a; padding: 1.1rem 0; display: block; }
[data-theme="dark"] .radhe-rule { background: linear-gradient(to right, transparent, #e8c46a 30%, #e8c46a 70%, transparent); }
[data-theme="dark"] .radhe-text { color: #e8c46a; }
```

---

## Global text rules

These apply sitewide and must be preserved in all files:

- **Justified paragraphs** — `p { text-align: justify; }` is set in every file's `<style>` block.
- **No em-dashes** — Use `, ` (comma-space) instead of ` — ` or `&mdash;` everywhere. This is a deliberate style choice.

---

## Typography

Two Google Fonts families used sitewide:
- `Cormorant Garamond` (serif, `var(--serif)`) — headings, overlays, pull quotes
- `Inter` (sans-serif, `var(--sans)`) — body, nav, labels

---

## Accent color

Light mode: `--accent: #6b5443` (warm brown). Dark mode: `--accent: #c69a7a` (lighter tan). Used for highlights and diamond separators in the marquee.

---

## Image patterns

### Venture cover image (`.v-cover`)

Used in venture pages (`pujan-energy.html`, `lenskart.html`) between the hero section and the overview section.

```css
.v-cover { width: 100%; height: clamp(260px, 42vw, 560px); overflow: hidden; }
.v-cover img { width: 100%; height: 100%; object-fit: cover; object-position: center 40%; display: block; }
```

```html
<div class="v-cover">
  <img src="image.jpg" alt="Description" loading="lazy">
</div>
```

Image spec: 1920×928px, JPEG, warm-graded to match `--accent: #6b5443`. Use Python PIL: `ImageEnhance.Color(0.82)`, `ImageEnhance.Brightness(0.93)`, warm overlay blend `#af8058` at alpha 0.10.

### Portrait circle

Used in `index.html` hero and `journey.html` hero.

```css
.j-portrait {
  position: absolute; top: 5.75rem; right: calc(var(--pad) + 0.5rem);
  width: clamp(96px, 10.5vw, 148px); height: clamp(96px, 10.5vw, 148px);
  border-radius: 50%; overflow: hidden; border: 1px solid var(--line);
  background: var(--bg-deep);
  box-shadow: 0 2px 24px color-mix(in srgb, var(--ink) 6%, transparent);
}
.j-portrait img { width: 100%; height: 100%; object-fit: cover; object-position: center top; display: block; }
```

- `pulkit.jpg` — front-facing DSLR portrait, used in `index.html` hero
- `pulkit-right.jpg` — side-profile portrait (500×500px), used in `journey.html` hero circle

---

## Journey page specifics (`journey.html`)

### Timeline order
**Chronological (oldest first)**: 2007 HSC → 2010 BBA → 2013 AIESEC → 2013 Research → 2014 Macau → 2015 Lenskart → 2018 Delhi → 2018 Ximivogue → 2019 Pujan Energy → 2021 Candy Floss → 2026 Today.

### Invisible venture links (`.t-venture-link`)
Venture names in timeline items are wrapped in `<a>` tags but styled to be completely invisible — no underline, no color change, no cursor change. CSS:

```css
.t-venture-link { color: inherit; text-decoration: none; cursor: inherit; }
.t-venture-link:hover, .t-venture-link:visited, .t-venture-link:focus { color: inherit; text-decoration: none; outline: none; }
```

### Animated footprints (`.j-fps`)
SVG footprints in the hero, walking diagonally bottom-center → top-right. Key implementation notes:
- `preserveAspectRatio="none"` so footprint positions map to screen percentage correctly
- Animation is opacity-only (`fp-loop` keyframe), **not** transform-based — transform inside keyframes caused the animation to silently fail in some browsers
- Negative `animation-delay` values bake phase offsets for seamless infinite loop
- Footprints positioned in the right 35% of the viewBox (x > 786 in a 1200-wide viewBox) to avoid overlapping text

---

## Security

All 6 HTML files include three security meta tags (added June 2025):
1. **CSP** — restricts resource origins, blocks connect/form/base injection
2. **Referrer-Policy** — `strict-origin-when-cross-origin`
3. **Permissions-Policy** — camera, mic, geolocation, payment all disabled

Note: `X-Frame-Options` / `frame-ancestors` require HTTP response headers — meta tags don't work for those. If hosted on Netlify, add a `_headers` file or `netlify.toml` for full clickjacking protection.

The contact email in `index.html` is HTML-entity encoded to deter simple bot scrapers.

---

## Asset inventory

| File | Size | Description |
|---|---|---|
| `pulkit.jpg` | 6.1 MB | Front-facing DSLR portrait (original full resolution) |
| `pulkit-right.jpg` | 25 KB | Side-profile portrait, 500×500px, cropped to face |
| `pujan-solar.jpg` | 786 KB | Solar farm installation photo, 1920×928px, warm-graded |
| `lenskart-store.jpg` | 386 KB | 4-panel store collage, 1920×928px, warm-graded |
| `favicon.ico` | 3 KB | Multi-size ICO (16/32/48px), memoji |
| `favicon-32x32.png` | 2 KB | 32×32 PNG favicon |
| `apple-touch-icon.png` | 29 KB | 180×180 PNG, memoji |
