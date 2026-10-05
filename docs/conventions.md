# Conventions

## Editing

- Change `concept-build.py` for page content and shared HTML. Change the two
  CSS or two JavaScript source files for shared design or behaviour.
- Run `python3 concept-build.py --production` after every source edit and review
  affected generated pages. Do not make durable edits only in generated HTML.
- Keep `PAGE_SLUGS` in the builder and `sitePages` in the transition script in
  sync when adding or removing a page.
- Preserve `legacy-source/` as fixed content provenance. If claims change,
  update the builder's current copy explicitly rather than rewriting history.

## Page requirements

- Every page retains the favicon links, CSP, referrer and permissions policies,
  theme toggle, motion toggle, contact section, and centered
  `|| राधे राधे ||` footer greeting with dividers.
- Production HTML must use normal `.html` links and `index, follow` metadata.
  Local `concept-*.html` previews use `noindex, nofollow` metadata.
- All paragraphs are justified. Do not use em dashes in visible text.
- Mark Hindi content `lang="hi"` and Gujarati content `lang="gu"` so the
  self-hosted Tiro Devanagari Hindi and Rasa fonts render correctly.
- Keep animation optional: `prefers-reduced-motion` and the on-page motion
  control must leave content and navigation usable.

## Review

Check local links and assets on all 13 pages, then inspect the home, work,
journey, about, and a venture page on desktop and mobile. Test navigation,
filters, dark mode, and reduced motion before deploying.
