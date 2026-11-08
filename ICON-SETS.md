# Xymon status icon sets: implementation guide

How to add the icon sets from the Xymon documentation preview
(https://stefcoene.github.io/xymon-docs-preview/icons/) to another web page or app.
The reference implementation is in this repository:

- images: [`docs/images/status/`](docs/images/status/)
- CSS: [`docs/stylesheets/xymon.css`](docs/stylesheets/xymon.css), section "Status icons" onwards
- JS: [`docs/javascripts/xymon.js`](docs/javascripts/xymon.js) (switcher, remembered choice)
- HTML generation: [`hooks/xymon_matrix.py`](hooks/xymon_matrix.py) (`GLYPH`, `_glyphs`, `_icon_table`)

## 1. Concepts

Every icon carries two pieces of information:

| | Values |
|---|---|
| **Status** | `green`, `yellow`, `red`, `purple`, `clear` (Xymon also has `blue`: only the Christmas set has an image for it) |
| **Recent** | the status changed recently (Xymon: `*-recent.gif`, see `xymongen --recentgifs`) |

On top of that, the viewer chooses:

| Choice | Values | Default |
|---|---|---|
| **Icon set** | `classic`, `watcher`, `vector`, `accessible`, `text`, `christmas`, `gifts`, `baubles` | `classic` |
| **Animate** | `off`, `on` | `off` (as in Debian's Xymon theme; many people dislike blinking) |

Animation rule, as in Xymon: **only problem colours move (yellow, red, purple)**. Green and clear stay still,
except where a set animates them itself (Watcher's recent icons pulse in every colour).
Never add a CSS blink to recent icons: in practice recent is mostly green, and green must not blink.

## 2. The icon is a character

Each icon is a `<span>` that contains a Unicode character. Image sets paint over it; the text set shows it.
The status then survives copy/paste into plain text and is read by screen readers.

| Status | Character | Recent |
|---|---|---|
| green | ✓ U+2713 | add `*` |
| yellow | ▲ U+25B2 | add `*` |
| red | ✕ U+2715 | add `*` |
| purple | ◆ U+25C6 | add `*` |
| clear | ○ U+25CB | add `*` |

```html
<span class="xm-dot red" title="...">✕</span>
<span class="xm-dot green recent" title="...">✓<span class="xm-r">*</span></span>
```

Do not use emoji (🟢 🔴): their look depends on the platform and CSS cannot recolour them.

## 3. Files per set

All 16×16 pixels, except the Christmas originals (24×24, scaled down by CSS). Paths are relative to `docs/images/status/`.

| Set | Still images | Animated images (used only with Animate on) | Notes |
|---|---|---|---|
| classic | `<status>.gif`, `<status>-recent.gif` | `animated/{yellow,red,purple}{,-recent}.gif` | The icons shipped with Xymon (`xymond/wwwfiles/gifs`). Stills are one chosen frame: yellow frame 0 (the "!"), red the last frame (big cross), purple frame 18 (filled box), recent faces frame 0. |
| watcher | `watcher/<status>.gif`, `watcher/<status>-recent.gif` | `watcher/animated/<status>-recent.gif` (all five colours) | Steven Aiello. The original recent GIFs pulse; the stills are frame 0. With Animate on, yellow/red/purple use the animated recent GIF for both normal and recent; green/clear only for recent. |
| vector | `vector/<status>.svg`, `vector/<status>-recent.svg`; also `blue`, `{yellow,red,purple}-ack`, `unknown`, `unknown-recent`, `arrow` (21×15), `zoom` for a full Xymon skin | none: CSS pulse | Stef Coene. Exported from the `<symbol>`s in dig-bollen `templates/_icons.html`, `currentColor` replaced by the Xymon colours. |
| accessible | `accessible/<status>.svg`, `accessible/<status>-recent.svg`; same extra files as vector | none: CSS pulse | Stef Coene. Okabe-Ito colours, from dig-bollen `templates/_icons_toegankelijk.html`. Recent = filled, older = hollow. |
| text | none | none: CSS blink | The character itself, coloured by CSS. |
| christmas | `christmas/{green,yellow,red}{,-recent}.gif`, `christmas/blue.gif`, page background `christmas/bkg.gif` | none: CSS blink | Henrik Størner, https://www.xymon.com/misc/Christmas.zip. **No purple or clear**: fall back to classic. |
| gifts | `gifts/<status>.gif` (one per colour) | none: CSS blink | Steve Dobbs (2003, deadcat.net). No recent images: show recent with a glow (`filter: drop-shadow(0 0 3px #fff6b0)`). |
| baubles | `baubles/<status>.png`, `baubles/<status>-recent.png` (also blue) | none: CSS blink | Bruno Manzoni. 16×16 PNG RGBA; recent adds a gold sparkle. |

Keep the `README.txt` files next to the images: they hold the makers' notes and licence statements.

## 4. CSS

Set the choices as attributes on `<html>`: `data-icons="<set>"` and `data-anim="on|off"`.

```css
/* Base: a 16px box, the character hidden but present */
.xm-dot {
  display: inline-block; width: 16px; height: 16px; vertical-align: middle; overflow: hidden;
  background: center / 16px 16px no-repeat; image-rendering: pixelated;
  color: transparent; font: 12px/16px Verdana, sans-serif; text-align: center; white-space: nowrap;
}
.xm-dot .xm-r { font-size: 0; }

/* Classic is the default (no attribute selector) */
.xm-dot.red { background-image: url("images/status/red.gif"); }
.xm-dot.red.recent { background-image: url("images/status/red-recent.gif"); }
/* ... same for every status ... */

/* Other sets override per set */
html[data-icons="watcher"] .xm-dot.red { background-image: url("images/status/watcher/red.gif"); }
html[data-icons="vector"] .xm-dot, html[data-icons="accessible"] .xm-dot { image-rendering: auto; }

/* Text set: show the character */
html[data-icons="text"] .xm-dot {
  background-image: none !important;   /* beats .xm-dot.<colour>.recent */
  width: auto; height: auto; overflow: visible; color: var(--xm-red);  /* per status */
  font-size: 1.15em; line-height: 1; font-weight: 700;
}
html[data-icons="text"] .xm-dot .xm-r { font-size: .6em; vertical-align: super; }

/* Animation: only yellow, red, purple */
@keyframes xm-blink { 50% { opacity: .2; } }
@keyframes xm-pulse { 0%, 100% { filter: drop-shadow(0 0 0 transparent); }
                      50% { filter: drop-shadow(0 0 4px var(--xm-c)); } }
html[data-anim="on"][data-icons="classic"] .xm-dot.red { background-image: url("images/status/animated/red.gif"); }
html[data-anim="on"]:not([data-icons="classic"], [data-icons="watcher"]) .xm-dot:is(.yellow, .red, .purple) {
  animation: xm-blink 1.2s steps(1, end) infinite;
}
html[data-anim="on"]:is([data-icons="vector"], [data-icons="accessible"]) .xm-dot:is(.yellow, .red, .purple) {
  overflow: visible; animation: xm-pulse 1.8s ease-in-out infinite;
}
```

The full rule set, including Watcher's animated GIFs, the Christmas fallback and background, and the colour
variables, is in `docs/stylesheets/xymon.css`.

## 5. JavaScript

Set the attributes **before the page renders** (in `<head>` or a script loaded early) to avoid a flash, and
remember the choice. Wrap storage in try/catch: it can be unavailable.

```js
(function () {
  var root = document.documentElement;
  try {
    root.setAttribute("data-icons", localStorage.getItem("xm-icons") || "classic");
    root.setAttribute("data-anim", localStorage.getItem("xm-anim") || "off");
  } catch (e) {
    root.setAttribute("data-icons", "classic");
    root.setAttribute("data-anim", "off");
  }
})();
```

Buttons: `<button data-icons="watcher">` and `<button data-anim="on">`; on click set the attribute on
`<html>`, store it, and update `aria-pressed`. See `xmToggle()` in `docs/javascripts/xymon.js`.

## 6. Pitfalls we hit

1. **Specificity.** `.xm-dot.green.recent` (3 classes) beats `html[data-icons="x"] .xm-dot.green` (1 attribute,
   1 class, 1 element). Every set that has its own rules must also write the `.recent` variant, or use
   `!important` like the text set.
2. **Choosing a still frame.** Do not pick frames automatically (e.g. "most pixels"). The red animation
   shrinks the cross to an empty octagon, yellow flashes brackets, purple fills and empties. Look at the
   frames and pick the one that says what the icon means.
3. **GIF frames are composited.** Extract frames with Pillow's `ImageSequence.Iterator(...)` and
   `.convert("RGBA")`; a bare `seek()` + `save()` can give a partial frame.
4. **Animated GIFs in a set.** Check every GIF for frames (`Image.open(f).n_frames > 1`). Watcher's
   `*-recent.gif` were animated and kept moving with Animate off.
5. **Caching.** If you serve from GitHub Pages (10-minute cache), version the CSS/JS URLs with a content
   hash (`xymon.css?v=<sha1>`), or the browser pairs new pages with an old script. Images keep their name,
   so a changed image can take up to 10 minutes to show.
6. **Reduced motion.** Animate is an explicit choice, so it overrides `prefers-reduced-motion`; with the
   default (off) nothing moves anyway.

## 7. Credits to show

| Set | Credit |
|---|---|
| Classic | Shipped with Xymon; collected by Henrik Størner (2004–2005) from Big Sister and deadcat.net collections ([README](https://github.com/xymon-monitoring/xymon/blob/main/xymond/wwwfiles/gifs/README)) |
| Watcher | Steven Aiello (2007–2008), Xymonton add-on [sa_icons](https://wiki.xymonton.org/doku.php/addons:sa_icons): "Use them as you like" |
| Vector, Accessible | Stef Coene |
| Christmas | Henrik Størner (2007), [Christmas.zip](https://www.xymon.com/misc/Christmas.zip) |
| Gifts | Steve Dobbs (2003), [gifts.tar.gz](https://web.archive.org/web/20080726061802if_/http://www.deadcat.net/40/gifts.tar.gz) |
| Baubles | Bruno Manzoni |

## 8. Prompt for a new Claude session

> Implement the Xymon status icon sets in `<project>`, following
> https://github.com/StefCoene/xymon-docs-preview/blob/main/ICON-SETS.md. Copy the images from
> `docs/images/status/` in that repository (with their README files). Our status icons are rendered in
> `<file/template>`; render each one as a `<span class="xm-dot <status>[ recent]">` with the Unicode
> character inside, add the CSS and the switcher (icon set + Animate, default classic/off, remembered in
> localStorage), and add a page or panel that shows every set, status and state, like
> https://stefcoene.github.io/xymon-docs-preview/icons/. Credit the makers as in section 7. Check each
> GIF for animation frames, and verify with a screenshot that nothing moves with Animate off.
