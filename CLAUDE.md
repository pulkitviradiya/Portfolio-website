# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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

### Mandatory page requirements

Every new page **must** include both of the following — no exceptions:

#### 1. Favicon (in `<head>`, after the viewport meta tag)
```html
<link rel="icon" type="image/x-icon" href="favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
```
Files live at the repo root: `favicon.ico`, `favicon-32x32.png`, `apple-touch-icon.png` (memoji, transparent background).

#### 2. Radhe Radhe greeting (placed immediately above `<footer>`)
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

### Typography

Two Google Fonts families used sitewide:
- `Cormorant Garamond` (serif, `var(--serif)`) — headings, overlays, pull quotes
- `Inter` (sans-serif, `var(--sans)`) — body, nav, labels

### Accent color

Light mode: `--accent: #6b5443` (warm brown). Dark mode: `--accent: #c69a7a` (lighter tan). Used for highlights and diamond separators in the marquee.
