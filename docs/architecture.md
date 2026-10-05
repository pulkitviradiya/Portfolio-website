# Architecture

## Site

This is a static portfolio with 13 HTML pages at the repository root:

- Home: `index.html`
- Work and story: `work.html`, `journey.html`, `about.html`, `off-duty.html`
- Early chapters: `education.html`, `cairo.html`, `research.html`
- Ventures: `candy-floss.html`, `pujan-energy.html`, `lenskart.html`,
  `ximivogue.html`, `ps-coffee.html`

Each page is standalone: styles are in a `<style>` element and JavaScript is
inline near the end of `<body>`. This preserves direct local-file previews and
requires no runtime framework or backend.

## Build source

`concept-build.py --production` generates all production HTML files. It inlines
`concept-style.css`, `concept-editorial.css`, `concept-script.js`, and
`concept-editorial.js`, and uses `concept-icons.json` for SVG icons. Running the
same script without flags generates ignored `concept-*.html` review pages.

The builder reads detailed case-study and timeline content from frozen
`legacy-source/*.html` files. These inputs are not production pages. The entire
former site is preserved on the remote Git branch
`archive/pre-concept-2026-10-06` and in a local tar archive noted in
`AGENTS.md`.

## Assets and deployment

Images, icons, and self-hosted WOFF2 fonts live at the root. The Latin fonts are
Instrument Serif and Space Grotesk; Hindi uses Tiro Devanagari Hindi, Gujarati
uses Rasa. Font and icon licenses are stored beside the assets.

GitHub `main` is linked to Vercel project `portfolio-website`. The public
domain is `www.pulkitviradiya.in`. `.vercelignore` excludes source files,
preview HTML, and frozen legacy inputs from the static deployment. The
generated pages remain the deployable root output.
