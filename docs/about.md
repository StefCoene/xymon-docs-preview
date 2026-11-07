# About this preview

This site is an **unofficial proposal** for one central documentation site for Xymon. If the Xymon maintainers like the idea, it can move to `xymon-monitoring.github.io`.

## Where the content comes from

Every build pulls the documentation straight from the source repositories, so nothing here is a hand-made copy that drifts out of date.

| Section | Source |
|---|---|
| Manual and man pages, dev | [`xymon`](https://github.com/xymon-monitoring/xymon), `docs/` on `main` |
| Manual and man pages, 4.3 | [`xymon`](https://github.com/xymon-monitoring/xymon), `docs/` at tag `rel-4.3.31` |
| Guides, project pages, PowerShell client | [`xymon-wiki`](https://github.com/xymon-monitoring/xymon-wiki) |
| Plugins | [`xymon-plugins`](https://github.com/xymon-monitoring/xymon-plugins) |
| Overview, download, community, clients | Written for this site |

The site rebuilds on every push and once a night.

## How the status colours work

The grid on the [home page](index.md) is defined in `matrix.yml`. A build hook works out each colour:

<pre class="xm-msg">red     the page the grid points to does not exist
yellow  the source file has not changed in five years or more
green   the page exists and changed more recently
purple  external content that has not been migrated here
clear   no page of this type for this topic
blinking: the source changed in the last 30 days</pre>

So the grid doubles as a to-do list. Switch to **non-green only** to see what needs work.

## Status icons

Four icon sets are available; switch between them above the grid on the home page. Your choice is remembered in your browser.

| Set | Made by |
|---|---|
| Classic | Stef Coene. Pixel icons in the traditional Xymon style: symbols for a status, faces for a recent change. |
| Vector | Stef Coene. Soft, rounded versions of the classic shapes. |
| Accessible | Stef Coene. A distinct shape and symbol for each status, in colour-blind-safe colours; a recent change is shown filled, an older one hollow. |
| Watcher | Steven Aiello (2007–2008), from the Xymonton add-on [sa_icons](https://wiki.xymonton.org/doku.php/addons:sa_icons). One shape per colour, so the grid also works for colour-blind readers. His [README](images/status/watcher/README.txt): "Use them as you like". |

## Built with

[MkDocs](https://www.mkdocs.org/) and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), hosted on GitHub Pages. Source: [StefCoene/xymon-docs-preview](https://github.com/StefCoene/xymon-docs-preview).
