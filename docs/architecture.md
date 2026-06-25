# Architecture

## Folder structure

```
Portfolio-website/
├── index.html            Homepage — hero, about, ventures grid, contact
├── journey.html          Long-form career timeline with animated hero
├── candy-floss.html      Venture case study — Candy Floss fashion brand
├── lenskart.html         Venture case study — Lenskart franchise
├── ximivogue.html        Venture case study — Ximivogue brand
├── pujan-energy.html     Venture case study — Pujan Energy (solar)
├── pulkit.jpg            Front-facing DSLR portrait (6.1 MB — needs resize)
├── pulkit-right.jpg      Side-profile portrait, 500×500 px
├── pujan-solar.jpg       Solar farm cover image, 1920×928 px
├── lenskart-store.jpg    4-panel store collage, 1920×928 px
├── favicon.ico           Multi-size ICO (16/32/48 px), memoji
├── favicon-32x32.png     32×32 PNG favicon
├── apple-touch-icon.png  180×180 PNG, memoji
├── .gitignore
├── CLAUDE.md             AI session instructions and project guide
├── AGENTS.md             Same as CLAUDE.md, branded for Codex
├── MEMORY.md             Running session notes and current-state facts
├── ARCHIVE.md            Historical entries archived from MEMORY.md
├── README.md             Minimal stub
└── docs/
    ├── architecture.md   This file
    ├── conventions.md    Naming and code conventions
    └── tasks.md          Open tasks and known issues
```

## Tech stack

| Technology | Role | Reason |
|---|---|---|
| Plain HTML | Page structure | No build step needed; site is content-only |
| Inline CSS (`<style>`) | All styling per page | Self-contained files, no shared stylesheet |
| Inline JS (`<script>`) | All behaviour per page | No framework, no bundler |
| CSS custom properties | Design tokens (colours, spacing, fonts) | Enables dark mode without class duplication |
| Google Fonts | `Cormorant Garamond` + `Inter` | Matches editorial, refined aesthetic |
| `IntersectionObserver` | Scroll-triggered reveal animations | Native browser API, no library required |
| Python PIL | Image processing (offline, not in site) | Cover-crop, colour grading, favicon generation |

## Design tokens (`:root`)

| Token | Light value | Dark value | Purpose |
|---|---|---|---|
| `--bg` | `#f3f1ea` | `#161614` | Page background |
| `--bg-deep` | `#ebe8df` | `#1f1f1d` | Inset / card background |
| `--bg-card` | `#ffffff` | `#1f1f1d` | Card surfaces |
| `--ink` | `#1a1a1a` | `#f3f1ea` | Primary text |
| `--ink-soft` | `#4a4a4a` | `#c9c6bd` | Secondary text |
| `--ink-mute` | `#8a8a85` | `#7a7872` | Muted / labels |
| `--line` | `#d8d4c8` | `#484840` | Dividers, borders |
| `--accent` | `#6b5443` | `#c69a7a` | Warm brown highlight |
| `--serif` | `Cormorant Garamond` | same | Headings, pull quotes |
| `--sans` | `Inter` | same | Body, nav, labels |
| `--maxw` | `1240px` | — | Max content width |
| `--pad` | `clamp(1.25rem, 4vw, 2.5rem)` | — | Horizontal page padding |
| `--section-pad` | `clamp(4rem, 9vw, 7rem)` | — | Vertical section spacing |

## Third-party services

| Service | Usage |
|---|---|
| Google Fonts (fonts.googleapis.com) | Serves `Cormorant Garamond` and `Inter` at runtime |
| LinkedIn (linkedin.com) | Outbound profile link only — no data exchanged |

No backend, no database, no analytics, no tracking, no CMS.

## Security

Three meta tags on every page (added 2026-06-25):
- **CSP** — `default-src 'self'`, restricts fonts to Google, blocks connect/form/base injection
- **Referrer-Policy** — `strict-origin-when-cross-origin`
- **Permissions-Policy** — camera, mic, geolocation, payment all disabled

Note: `X-Frame-Options` / `frame-ancestors` require HTTP headers, not meta tags. Add via `_headers` file if deploying to Netlify/Vercel.
