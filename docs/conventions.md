# Conventions

## File naming

- HTML files: `kebab-case.html` — e.g. `candy-floss.html`, `pujan-energy.html`
- Image files: `kebab-case.jpg` — e.g. `pujan-solar.jpg`, `lenskart-store.jpg`
- Portrait images follow subject-descriptor pattern: `pulkit.jpg`, `pulkit-right.jpg`
- No subdirectories for HTML or images — everything at repo root

## CSS class naming

BEM-lite: `block` or `block-element`. No `block__element--modifier` syntax.

| Prefix | Scope | Examples |
|---|---|---|
| *(none)* | Global / shared | `container`, `reveal`, `section-label`, `pullquote` |
| `hero-` | Homepage hero | `hero-grid`, `hero-portrait`, `hero-eyebrow` |
| `v-` | Venture pages (all case studies) | `v-hero`, `v-cover`, `v-overview`, `v-stats-hero`, `v-highlight`, `v-outcome` |
| `j-` | Journey page | `j-hero`, `j-deco`, `j-fps`, `j-fp`, `j-portrait` |
| `t-` | Timeline items (inside journey) | `t-item`, `t-title`, `t-venture-link` |
| `nav-` | Navigation | `nav-logo`, `nav-right` |
| `menu-` | Mobile nav overlay | `menu-overlay`, `menu-pill` |
| `radhe-` | Footer Radhe Radhe block | `radhe-section`, `radhe-rule`, `radhe-text` |

## Animation conventions

- Scroll reveals: add class `reveal` to any element. JS `IntersectionObserver` adds `.in` when visible, triggering `opacity 0→1` + `translateY 24px→0` transition.
- Stagger siblings with `delay-1` through `delay-4` (100 ms increments).
- Infinite SVG animations: use **opacity-only keyframes**. Never put `transform` or `transform-origin` inside `@keyframes` — browsers silently drop the entire animation.
- Infinite stagger offset: use negative `animation-delay` to phase elements within a shared cycle.

## Dark mode

- Theme stored in `localStorage('theme')` and applied as `data-theme="light|dark"` on `<html>`.
- All dark overrides live in a `[data-theme="dark"]` block in the same `<style>` tag — no separate dark stylesheet.
- First visit respects `prefers-color-scheme` via `window.matchMedia`.

## Per-page structure order

Every HTML file follows this structure top to bottom:

1. `<!DOCTYPE html>` + `<html data-theme="light">`
2. `<head>` — charset, viewport, security meta tags, favicon links, description, title, Google Fonts, `<style>`
3. `<body>` — nav, page content sections, Radhe Radhe block, footer
4. `<script>` — year inject, theme toggle, scroll nav, menu overlay, reveal observer

## Shared blocks (copy verbatim, never abstract)

These blocks are duplicated across all 6 files. When changing one, change all:
- Nav (`#nav`, `.nav-logo`, `.menu-pill`, `.menu-overlay`)
- Theme toggle JS
- Scroll nav JS
- Reveal observer JS
- Radhe Radhe footer block + CSS

## Mandatory elements for every new page

See CLAUDE.md §"Mandatory page requirements" for the exact HTML to copy. In brief:
1. Security meta tags (CSP + Referrer-Policy + Permissions-Policy) after viewport
2. Three favicon `<link>` tags after security meta tags
3. Radhe Radhe block immediately above `<footer>`

## Invisible hyperlinks (venture name links in timeline)

To make a link visually invisible (clickable but shows no underline or colour change):
```css
.t-venture-link { color: inherit; text-decoration: none; cursor: inherit; }
.t-venture-link:hover, .t-venture-link:visited, .t-venture-link:focus { color: inherit; text-decoration: none; outline: none; }
```

## Typography rules

- All `<p>` text: `text-align: justify`
- No em-dashes (`—` / `&mdash;`) anywhere — use `, ` (comma-space) instead

## Image conventions

- Cover images for venture pages: 1920×928 px JPEG, warm-graded (see MEMORY.md for PIL params)
- Portrait circles: 500×500 px JPEG, face centred, `object-position: center top` in CSS
- All images: `loading="lazy"` attribute, descriptive `alt` text
