# Icon sets and text icons in Xymon itself: what the source code needs

The documentation preview (https://stefcoene.github.io/xymon-docs-preview/icons/) shows several icon
sets, a text variant, and an Animate switch, chosen per viewer in the browser. This note lists what Xymon
already supports, and what would have to change in the C code to support the rest.
Line numbers refer to `xymon-monitoring/xymon` main at commit `e9059d5d` (2026-11-07).

## 1. What Xymon can do today (no code change)

| Setting | Where | Effect |
|---|---|---|
| `XYMONSKIN` | `lib/environ.c:63`, default `$XYMONSERVERWWWURL/gifs`; documented in `xymonserver.cfg(5)` | URL of the directory the icons load from. Also sets `XYMONBODYCSS` (`$XYMONSKIN/xymonbody.css`, `lib/environ.c:154`). |
| `IMAGEFILETYPE` | `lib/environ.c:121`, default `gif`; **undocumented** | Extension of the icon files (`lib/color.c:118`), and of `arrow` (`lib/eventlog.c:840`) and `zoom` (`lib/xymonrrd.c:336`, `web/showgraph.c:715`). `IMAGEFILETYPE=svg` makes Xymon request `red.svg`. |
| `DOTWIDTH`, `DOTHEIGHT` | `lib/environ.c:119-120`, default 16 | `WIDTH`/`HEIGHT` of every icon `<IMG>`; `xymongen` also uses `DOTWIDTH` for column widths (`xymongen/pagegen.c:350`, `:482`). |
| `xymongen --recentgifs` | `xymongen/xymongen.c:301`, `lib/color.c:21` | Use `<colour>-recent` for a status that changed recently. |
| `xymongen --dialupskin=`, `--reverseskin=` | `xymongen/loaddata.c:300-301` | Another skin directory for tests with the `D` or `R` flag. |

So **every image set from the preview can already be used as a skin**: put the files in a directory, set
`XYMONSKIN` to its URL, and `IMAGEFILETYPE=svg` (or `png`) when needed. What a skin directory must
contain is listed in `TODO.md` ("Docs page: Using another icon set").

What is **not** possible today:

1. **Text icons.** Xymon always writes an `<IMG>`; there is no way to output a character instead.
2. **A per-viewer choice** of icon set or animation. The skin is set per installation, and `xymongen`
   writes static HTML. A site can only offer a second look by running a second `xymongen` with another
   `XYMONSKIN` into another directory.
3. **Animate on/off.** The classic yellow, red and purple GIFs are animated. The only way to stop them is a
   skin with still images (as the Debian theme does).

## 2. Step 1: one function that writes the icon

`dotgiffilename()` is called in **28 places** in 8 files. Almost every call site builds the `<IMG>` tag by
hand, with `xgetenv("XYMONSKIN")`, `DOTHEIGHT` and `DOTWIDTH`:

| File | Calls | What |
|---|---|---|
| `xymongen/pagegen.c` | 8 | Overview pages, summaries, report pages (`:419`, `:560`, `:567`, `:618`, `:873`), info/trends/client column images (`:455-457`) |
| `lib/reportlog.c` | 7 | Availability report and its legend (`:64-74`, `:207`) |
| `web/history.c` | 7 | History page and its legend (`:90-100`, `:477`) |
| `lib/eventlog.c` | 2 | Event log: old and new colour (`:836`, `:844`) |
| `lib/htmllog.c` | 1 | Status page: `&red` etc. in the status text (`:154`) |
| `lib/acklog.c` | 1 | Acknowledgement log (`:219`) |
| `web/criticalview.c` | 1 | Critical systems view (`:278`) |
| `web/svcstatus-info.c` | 1 | The info column (`:375`) |

Add one function to `lib/color.c` (declared in `lib/color.h`) and use it everywhere:

```c
/* Returns the HTML for one status icon, in a static buffer. */
char *statusicon(char *skin, int color, int acked, int oldage, char *alttext);
```

For image output it returns what is written today, plus a `class` attribute:

```html
<IMG SRC="/xymon/gifs/red-recent.gif" CLASS="xmdot red recent" ALT="red, recent" TITLE="..." HEIGHT="16" WIDTH="16" BORDER=0>
```

The output stays the same apart from the class, so this step changes nothing visible. It is a pure refactor
and can be merged on its own. The class names (`xmdot`, the colour name, `recent`, `ack`) are what the next
steps hang on.

Special cases to keep:

- `infocolumngif`, `trendscolumngif`, `clientcolumngif` (`xymongen/pagegen.c:455-457`): the info,
  trends and client columns show a fixed image (default the green dot, overridable with `INFOCOLUMNGIF`,
  `TRENDSCOLUMNGIF`, `CLIENTCOLUMNGIF`) that is a link, not a status.
  Give them their own class (`xmdot info`, `xmdot trends`, `xmdot client`) so text mode can show something
  else for them (see 3.3).
- The per-test skin from `--dialupskin` / `--reverseskin` (`e->skin`): pass it as `skin`.
- Report pages (`reportstart > 0`) use `oldage = 1` for green and clear: keep that logic at the call site.

## 3. Step 2: text icons (`ICONSTYLE=text`)

### 3.1 Setting

A new setting in `xymonserver.cfg`, added to the defaults in `lib/environ.c` and documented in
`xymonserver.cfg(5)`:

```
ICONSTYLE="image"     # image (default) or text
```

### 3.2 Output

With `ICONSTYLE=text`, `statusicon()` returns a span with a character instead of an image:

```html
<span class="xmdot red recent" title="cpu: red, recent">&#x2715;<span class="r">*</span></span>
```

Use **numeric character references** (`&#x2715;`), not UTF-8 bytes: the header templates
(`xymond/webfiles/*_header`) do not declare a charset, so raw UTF-8 could show as mojibake.

| Status | Character | Reference | Notes |
|---|---|---|---|
| green | ✓ | `&#x2713;` | |
| yellow | ▲ | `&#x25B2;` | |
| red | ✕ | `&#x2715;` | |
| purple | ◆ | `&#x25C6;` | |
| clear | ○ | `&#x25CB;` | |
| blue | ■ | `&#x25A0;` | a filled shape like ▲ and ◆; the square matches the Vector and Accessible sets |
| recent | `*` after the character | | only with `--recentgifs`, as now |
| acked | the character in brackets, e.g. `(✕)`, class `ack` (dimmed) | | only yellow, red and purple can be acknowledged |
| unknown | ? | `?` | `unknown-recent`: `?*` |
| arrow | → | `&#x2192;` | event log, "from → to" |
| zoom | ⊕ | `&#x2295;` | graphs |

The character is the information and survives copy/paste into mails and tickets; screen readers read it.
Do not use emoji (🟢, ⏸, 🔍): their look depends on the platform, CSS cannot recolour them, and without an
emoji font they show as empty boxes. The icons page shows all of these in the **text** column of
"Complete Xymon skin".

### 3.3 CSS

Add the rules to `xymond/wwwfiles/gifs/xymonbody.css` (loaded on every page through `&XYMONBODYCSS`):

```css
.xmdot { display: inline-block; min-width: 16px; text-align: center; font-weight: bold; line-height: 1; }
.xmdot.green  { color: #00cc00; }  .xmdot.yellow { color: #ffcc00; }
.xmdot.red    { color: #ff0000; }  .xmdot.purple { color: #cc66ff; }
.xmdot.clear  { color: #c0c0c0; }  .xmdot.blue   { color: #3399ff; }
.xmdot .r { font-size: .6em; vertical-align: super; }
.xmdot.ack { opacity: .65; }
```

`min-width` keeps the column widths that `xymongen` computes from `DOTWIDTH`.

For the info, trends and client columns, text mode needs another character, because a green ✓ there would
look like a status. Proposal: `&#x24D8;` ⓘ for info, `&#x2197;` ↗ for trends, `&#x2630;` ☰ for client.

### 3.4 What else is affected

- **Legends** on the history and report pages (`web/history.c:90-100`, `lib/reportlog.c:64-74`) go through
  `statusicon()` like everything else, so they follow automatically.
- **`&red` in status messages** (`lib/htmllog.c:154`) is the same; text icons then also appear inside the
  status text.
- **Alerts, mails and RSS** are plain text or use their own format: not affected.
- **`arrow` and `zoom`** (event log, graphs) stay images; they are not statuses.
- **Static pages** generated by `xymongen` contain the text icons literally; switching back to images
  needs a new `xymongen` run (happens every cycle anyway).

## 4. Step 3 (optional): choice per viewer and Animate

With the classes from step 1, the browser can change the look without Xymon knowing: this is exactly what
the preview does.

1. `statusicon()` always writes the **text span** (3.2), also in image mode, and the skin's CSS paints
   the image over the character:
   ```css
   .xmdot { width: 16px; height: 16px; overflow: hidden; color: transparent;
            background: center / 16px 16px no-repeat; }
   .xmdot.red { background-image: url("red.gif"); }
   .xmdot.red.recent { background-image: url("red-recent.gif"); }
   ```
   This is simpler than switching between `<img>` and `<span>`, and the character still survives
   copy/paste. Downside: older custom skins that only contain images then need this CSS. That is a reason
   to keep `ICONSTYLE=image` as the default and make this a third style (`ICONSTYLE=css`).
2. A small script in the header templates (`xymond/webfiles/stdnormal_header` etc.) reads a cookie or
   `localStorage` value and sets `<html data-icons="watcher" data-anim="off">`. The skins then live side by
   side under `$XYMONSERVERWWWURL/skins/<name>/`, and the CSS selects by attribute:
   `html[data-icons="watcher"] .xmdot.red { background-image: url("../skins/watcher/red.gif"); }`.
3. **Animate** per viewer needs two images per moving colour (still and animated), as the preview has for
   classic (`images/status/` and `images/status/animated/`), or a CSS animation for sets without animated
   files. Only yellow, red and purple move; green and clear never do.
4. A small menu entry or a settings page to choose (the preview uses two rows of buttons).

The preview implements all of this in the browser; the code and pitfalls are in `ICON-SETS.md`
(`docs/stylesheets/xymon.css`, `docs/javascripts/xymon.js`).

## 5. Suggested order of pull requests

| # | Change | Risk |
|---|---|---|
| 1 | Document `IMAGEFILETYPE` in `xymonserver.cfg(5)` | none: docs only |
| 2 | Ship extra skins under `xymond/wwwfiles/skins/` (classic still, Watcher, SVG sets, Christmas) and a docs page "Using another icon set" | none: files only, nothing changes unless `XYMONSKIN` is set |
| 3 | `statusicon()` refactor with `CLASS` attribute (section 2) | low: same output plus a class; check the 28 call sites |
| 4 | `ICONSTYLE=text` (section 3) | low: off by default |
| 5 | `ICONSTYLE=css` with per-viewer choice and Animate (section 4) | medium: touches the header templates and every skin |

Steps 1 and 2 need no C code. Steps 3 and 4 are small and independent of the preview. Step 5 only makes
sense if users want it.
