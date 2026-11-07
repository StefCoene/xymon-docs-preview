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
recent:   the source changed in the last 30 days</pre>

So the grid doubles as a to-do list. Switch to **non-green only** to see what needs work.

## Status icons

Every icon is a character as well as a picture: ✓ green, ▲ yellow, ✕ red, ◆ purple, ○ clear, followed by `*` when the source changed in the last 30 days. Copy the grid into a mail or a text file and the statuses come along; screen readers read them too. An icon set only changes how that character looks, so a new theme (like Henrik's Christmas set below) is a few lines of CSS and some images.

Switch sets above the grid on the home page. Your choice is remembered in your browser. Icons do not blink, unless you turn on **Blink recent changes**. Then only recent changes move: the pixel sets blink, the Vector and Accessible sets pulse with a glow in the status colour.

| Set | Made by |
|---|---|
| Classic | Stef Coene. Pixel icons in the traditional Xymon style: symbols for a status, faces for a recent change. Shown without animation. |
| Vector | Stef Coene. Soft, rounded SVG versions of the classic shapes. |
| Accessible | Stef Coene. SVG; a distinct shape and symbol for each status, in colour-blind-safe colours (Okabe-Ito); a recent change is shown filled, an older one hollow. |
| Watcher | Steven Aiello (2007–2008), from the Xymonton add-on [sa_icons](https://wiki.xymonton.org/doku.php/addons:sa_icons). One shape per colour, so the grid also works for colour-blind readers. His [README](images/status/watcher/README.txt): "Use them as you like". |
| Christmas | Henrik Størner, the author of Xymon (2007), from [Christmas.zip](https://www.xymon.com/misc/Christmas.zip) on xymon.com: baubles in the status colour, and a tree, a poinsettia or a bell for a recent change, on a fir-branch background. The set has no purple or clear icons, so the classic ones show there. [Notes](images/status/christmas/README.txt). |
| Gifts | Steve Dobbs (2003), gift boxes made "to get my grinch self into the Christmas spirit", from [gifts.tar.gz](https://web.archive.org/web/20080726061802if_/http://www.deadcat.net/40/gifts.tar.gz) on deadcat.net. One box per colour; a recent change gets a glow. His [read.me](images/status/gifts/README.txt). |
| Text | No images: the Unicode characters themselves, coloured with CSS. They scale and align with the text around them. |

## Built with

[MkDocs](https://www.mkdocs.org/) and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), hosted on GitHub Pages. Source: [StefCoene/xymon-docs-preview](https://github.com/StefCoene/xymon-docs-preview).
