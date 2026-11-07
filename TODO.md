# TODO

Open points for the documentation site. Feedback and pull requests welcome.

## Content

- [ ] **Wiki: link to the manual instead of `install.html.DIST`.**
  [how-to-compile-xymon.md, line 14](https://github.com/xymon-monitoring/xymon-wiki/blob/main/docs/guides/how-to-compile-xymon.md?plain=1#L14)
  links to the raw `docs/install.html.DIST` on GitHub. This site already rewrites the link to its own
  manual page (`hooks/xymon_matrix.py`, `_dist_links`). Fix it in the wiki once the site has its final
  address, so the wiki can link there.
- [ ] **Review the hand-written pages.** Clients, Download, Community and About were written from web
  research and nobody has checked them yet (projects still alive, versions, credits). Either add a
  `reviewed` flag that the status matrix shows, or leave unreviewed pages out of the navigation until
  someone checks them.
- [ ] Convert the HTML manual to Markdown, so it gets the site's layout and search.

## Site

- [ ] Decide the default for **Animate**: off now (as in Debian's Xymon theme), or on (as on a stock Xymon server).
- [ ] Move to `xymon-monitoring.github.io`: as a new repository, or by renaming `xymon-wiki` or the empty `xymon-site`?
- [ ] Merge `xymon-wiki` into this site, or keep both?
- [ ] Versioned docs with `mike` (4.3 / dev), instead of two copied directories.
- [ ] Custom domain (e.g. `docs.xymon.com`): who manages DNS for xymon.com?

## Community

- [ ] Ask the Xymonton admins whether their content may be migrated.
