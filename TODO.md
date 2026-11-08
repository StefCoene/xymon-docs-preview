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
- [ ] This site now shows the whole `xymon-wiki`, which is also its own site at
  https://xymon-monitoring.github.io/xymon-wiki/. Keep both, or retire the wiki site and keep the wiki repo as a source?
- [ ] Versioned docs with `mike` (4.3 / dev), instead of two copied directories.
- [ ] Custom domain (e.g. `docs.xymon.com`): who manages DNS for xymon.com?

## Icon sets

Xymon can already switch icon sets per installation, without code changes:
`XYMONSKIN` (documented in `xymonserver.cfg(5)`) sets the directory the icons load from,
`IMAGEFILETYPE` (default `gif`, `lib/environ.c` and `lib/color.c`; **undocumented**) sets the file
extension, so `IMAGEFILETYPE=svg` makes Xymon request `red.svg`, and `DOTWIDTH` / `DOTHEIGHT` set the size.

- [ ] **Decide what the docs show.** The preview offers several icon sets per viewer, which Xymon itself
  cannot do. Keep only the classic icons in the docs, or keep the sets and present them as optional
  skins (see below)? Discuss with the other developers.
- [ ] **Document `IMAGEFILETYPE`** in `xymonserver.cfg(5)` (pull request on `xymon`).
- [ ] **Docs page "Using another icon set"**: which files a skin directory needs, and how to set
  `XYMONSKIN` and `IMAGEFILETYPE`. A complete set has every colour (green, yellow, red, purple, blue,
  clear) as `<colour>` and `<colour>-recent`, `-ack` only for yellow, red and purple (only a problem
  can be acknowledged; Xymon's own `green-ack` and `blue-ack` are not needed), plus `unknown`,
  `unknown-recent`, `arrow`, `zoom`, `bkg-<colour>`, the `favicon-*.ico` files and `xymonbody.css`
  from `xymond/wwwfiles/gifs`. `IMAGEFILETYPE` also applies to `arrow` and `zoom` (so an SVG set needs
  `arrow.svg` and `zoom.svg`); the `bkg-*.gif` backgrounds are named in `xymonbody.css`, so a skin can keep them.
- [ ] **Complete the alternative sets as Xymon skins** and offer them as optional downloads on that page.
  The preview only copied what the status matrix uses; the originals have more. Still missing per set
  (`bkg-*`, `favicon-*` and `xymonbody.css` can come from classic):

  | Set | Blue | `-ack` | `unknown` | `arrow`, `zoom` | Other gaps |
  |---|---|---|---|---|---|
  | Classic | ok (Xymon's `gifs/`) | ok | ok | ok | complete; the preview only copied part |
  | Watcher | ok (dig-bollen) | ok | ok | ok | complete |
  | Vector, Accessible | ok | ok | ok | ok | complete (`scripts/make-svg-icons.py`) |
  | Baubles | ok | missing | missing | missing | |
  | Christmas | `blue` only, no `blue-recent` | missing | missing | missing | no purple, no clear |
  | Gifts | `blue.gif` in the original, not copied | missing | missing | missing | no `-recent` at all |

- [ ] **Animation in SVG sets**: Xymon has no Animate option, so an SVG set that should move needs the
  animation inside the SVG file (CSS or SMIL), only in the yellow, red and purple icons.
- [ ] Possible Xymon features, only if wanted: a per-viewer choice of icon set (the preview does it in the
  browser), and icons as text characters (Xymon writes `<img>` tags today). What the source code needs, step by step:
  [ICONS-IN-XYMON.md](ICONS-IN-XYMON.md).

## Community

- [ ] Ask the Xymonton admins whether their content may be migrated.
