# Portfolio website guidance

This is Pulkit Viradiya's static personal portfolio. `MEMORY.md` and
`ARCHIVE.md` contain older project notes; this file describes the current site.

## Before changing the site

- Read `MEMORY.md` at the start of a new session for background, but verify
  current architecture against this file and the source code.
- Run `git pull origin main` before editing in a new session. Another agent may
  have pushed changes to the same repository.
- Preserve unrelated working-tree changes. Do not edit `legacy-source/` as if
  it were the current website.

## Build and pages

`concept-build.py` is the source of the 13 standalone production HTML pages.
Shared CSS and JavaScript are in `concept-style.css`, `concept-editorial.css`,
`concept-script.js`, and `concept-editorial.js`; the builder inlines them into
each generated page. `concept-icons.json` supplies the local icon SVGs.

```sh
python3 concept-build.py --production  # writes index.html and 12 inner pages
python3 concept-build.py               # writes local concept-*.html previews
```

Production pages: `index.html`, `work.html`, `journey.html`, `about.html`,
`education.html`, `cairo.html`, `research.html`, `off-duty.html`,
`candy-floss.html`, `pujan-energy.html`, `lenskart.html`, `ximivogue.html`, and
`ps-coffee.html`. Edit the source files, rebuild, and review the generated HTML;
do not maintain the page copies independently.

`legacy-source/` contains frozen copies of the former journey and venture pages.
The builder reads their detailed content and chronology. The complete former
site is backed up on GitHub branch `archive/pre-concept-2026-10-06` and in
`/Users/pulkit/Code/Portfolio-website-archive/portfolio-pre-concept-2026-10-06.tar.gz`.

## Design and required elements

- Keep the approved warm, light editorial direction, with restrained accents.
- Latin type: Instrument Serif and Space Grotesk. Hindi: Tiro Devanagari Hindi.
  Gujarati: Rasa. The fonts are self-hosted with their licenses.
- Every page has the existing favicon links, security meta tags, dark-mode and
  motion controls, footer, and `|| राधे राधे ||` with dividers.
- Paragraphs are justified. Do not use em dashes in visible copy.
- Respect reduced-motion preferences and ensure every interactive control works
  without hover. The two-step Hindi loader appears on direct page loads and
  does not delay internal navigation.
- Keep case-study claims aligned with the legacy content; do not present plans
  or illustrative imagery as verified operating results.

## Release

The GitHub `main` branch is linked to the Vercel project `portfolio-website`.
`.vercelignore` excludes preview pages, build sources, and legacy inputs from
the public deployment. The public domain is `https://www.pulkitviradiya.in/`.
After pushing production changes, verify the Vercel deployment is Ready and
check the public domain before reporting the release complete.

Read `docs/architecture.md` and `docs/conventions.md` before structural work.
