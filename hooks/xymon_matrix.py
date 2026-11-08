"""MkDocs hook: render the Xymon-style status matrix on the home page.

Rows and cells come from matrix.yml. The colour of each cell is computed at build time:

  red     the target page does not exist in this build
  yellow  the source has not changed in STALE_YEARS years
  green   the page exists and its source changed more recently
  purple  external content that has not been migrated (set in matrix.yml)
  clear   no page of this type for this topic

A cell whose source changed in the last RECENT_DAYS days gets the "recent" marker.
"""

import datetime as dt
import hashlib
import html
import json
import os
import posixpath
import re
import subprocess

import yaml

PLACEHOLDER = "<!-- xymon-matrix -->"
SUMMARY = "<!-- xymon-summary -->"
STALE_YEARS = 5
RECENT_DAYS = 30
SEVERITY = ["red", "purple", "yellow", "green", "clear"]

_state = {"matrix": None, "dates": {}, "files": set()}


def _bust(entry, docs_dir):
    """Append ?v=<content hash> so browsers never pair new pages with a cached old script or stylesheet."""
    path = str(entry).split("?")[0]
    full = os.path.join(docs_dir, path)
    if not os.path.exists(full):
        return entry
    digest = hashlib.sha1(open(full, "rb").read()).hexdigest()[:10]
    if hasattr(entry, "path"):
        entry.path = f"{path}?v={digest}"
        return entry
    return f"{path}?v={digest}"


class _WikiLoader(yaml.SafeLoader):
    """Reads the wiki's mkdocs.yml, ignoring its !!python tags."""


_WikiLoader.add_multi_constructor("tag:yaml.org,2002:python/", lambda loader, suffix, node: None)


def _wiki_path(path):
    return "project/" + path[len("about/"):] if path.startswith("about/") else path


def _wiki_remap(items):
    out = []
    for item in items:
        if isinstance(item, str):
            out.append(_wiki_path(item))
        else:
            (title, value), = item.items()
            out.append({title: _wiki_remap(value) if isinstance(value, list) else _wiki_path(value)})
    return out


def _wiki_nav(nav, base):
    """Replace "wiki:<section>[,<section>...]" in the nav with sections of the wiki's own navigation."""
    try:
        with open(os.path.join(base, ".sources", "xymon-wiki", "mkdocs.yml"), encoding="utf-8") as fh:
            sections = {k: v for entry in yaml.load(fh, Loader=_WikiLoader)["nav"] for k, v in entry.items()}
    except (OSError, KeyError, TypeError):
        sections = {}

    def expand(value):
        if isinstance(value, list):
            return [walk(v) for v in value]
        if isinstance(value, str) and value.startswith("wiki:"):
            first, *rest = value[5:].split(",")
            items = _wiki_remap(sections.get(first, []))
            items += [{name: _wiki_remap(sections.get(name, []))} for name in rest]
            return items
        return value

    def walk(entry):
        if isinstance(entry, dict):
            return {k: expand(v) for k, v in entry.items()}
        return entry

    return [walk(e) for e in nav]


def on_config(config):
    base = os.path.dirname(config.config_file_path)
    config["nav"] = _wiki_nav(config["nav"], base)
    config["extra_css"] = [_bust(e, config["docs_dir"]) for e in config["extra_css"]]
    config["extra_javascript"] = [_bust(e, config["docs_dir"]) for e in config["extra_javascript"]]
    with open(os.path.join(base, "matrix.yml"), encoding="utf-8") as fh:
        _state["matrix"] = yaml.safe_load(fh)
    dates = os.path.join(base, ".sources", "dates.json")
    _state["dates"] = json.load(open(dates)) if os.path.exists(dates) else {}
    return config


def on_files(files, config):
    _state["files"] = {f.src_uri for f in files}
    return files


def _url(path):
    if path.endswith("/index.md") or path == "index.md":
        return path[: -len("index.md")]
    if path.endswith("/README.md"):
        return path[: -len("README.md")]
    if path.endswith(".md"):
        return path[:-3] + "/"
    return path


def _cell(spec, today):
    """Return (status, recent, href, title) for one matrix cell."""
    if spec is None:
        return "clear", False, None, "nothing of this type"
    if isinstance(spec, str):
        spec = {"path": spec}
    note = spec.get("note", "")
    if "url" in spec:
        status = spec.get("status", "green")
        title = note or ("external, not migrated" if status == "purple" else "external page")
        return status, False, spec["url"], title
    path = spec["path"]
    if path not in _state["files"]:
        return "red", False, None, f"missing: {path}"
    date = _state["dates"].get(path)
    status, recent = "green", False
    title = note
    if date:
        changed = dt.date.fromisoformat(date)
        age = (today - changed).days
        recent = age <= RECENT_DAYS
        if age > STALE_YEARS * 365:
            status = "yellow"
        title = (f"{note} · " if note else "") + f"last changed {date}"
    return spec.get("status", status), recent, _url(path), title


def _render(today):
    m = _state["matrix"]
    cols = m["columns"]
    counts = {s: 0 for s in SEVERITY}
    out = ['<div class="xm-matrix-wrap"><table class="xm-matrix">', "<thead><tr><th></th>"]
    out += [f"<th>{html.escape(c)}</th>" for c in cols]
    out.append("</tr></thead><tbody>")
    for group in m["groups"]:
        out.append(f'<tr class="xm-grp"><td colspan="{len(cols) + 1}">{html.escape(group["name"])}</td></tr>')
        for row in group["rows"]:
            cells, worst = [], "clear"
            for col in cols:
                status, recent, href, title = _cell(row.get("cells", {}).get(col), today)
                counts[status] += 1
                if SEVERITY.index(status) < SEVERITY.index(worst):
                    worst = status
                dot = f'<span class="xm-dot {status}{" recent" if recent else ""}" title="{html.escape(title)}"></span>'
                if href:
                    dot = f'<a href="{html.escape(href)}" aria-label="{html.escape(row["topic"])}: {col} ({status})">{dot}</a>'
                cells.append(f'<td class="c">{dot}</td>')
            out.append(f'<tr data-worst="{worst}"><td class="xm-topic">{html.escape(row["topic"])}</td>{"".join(cells)}</tr>')
    out.append("</tbody></table></div>")
    worst_all = next((s for s in SEVERITY if counts[s] and s != "clear"), "green")
    return "\n".join(out), counts, worst_all


# Imported pages: where each docs/ prefix comes from, so links to files this site does not
# publish (scripts, man sources, other wiki pages) can point to the file on GitHub instead.
SOURCES = {
    "plugins/": "https://github.com/xymon-monitoring/xymon-plugins/blob/main/",
    "guides/": "https://github.com/xymon-monitoring/xymon-wiki/blob/main/docs/guides/",
    "project/": "https://github.com/xymon-monitoring/xymon-wiki/blob/main/docs/about/",
    "contributing/": "https://github.com/xymon-monitoring/xymon-wiki/blob/main/docs/contributing/",
    "development/": "https://github.com/xymon-monitoring/xymon-wiki/blob/main/docs/development/",
    "clients/windows-powershell/": "https://github.com/xymon-monitoring/xymon-wiki/blob/main/docs/clients/windows-powershell/",
}
LINK = re.compile(r"\]\((?!https?:|mailto:|#|/)([^)\s]+)\)")


def _fix_links(markdown, src_uri):
    prefix = next((p for p in SOURCES if src_uri.startswith(p)), None)
    if prefix is None:
        return markdown
    here = posixpath.dirname(src_uri)

    def repl(m):
        target, _, anchor = m.group(1).partition("#")
        resolved = posixpath.normpath(posixpath.join(here, target))
        if resolved in _state["files"] or posixpath.join(resolved, "README.md") in _state["files"]:
            return m.group(0)
        moved = _wiki_path(resolved)  # wiki links to about/ pages, which live in project/ here
        if moved != resolved and moved in _state["files"]:
            return f"]({posixpath.relpath(moved, here or '.')}{'#' + anchor if anchor else ''})"
        rel = posixpath.relpath(resolved, prefix.rstrip("/"))
        base = SOURCES[prefix][len("https://github.com"):]
        path = posixpath.normpath(base + rel)
        return f"](https://github.com{path}{'#' + anchor if anchor else ''})"

    return LINK.sub(repl, markdown)


CHANGELOG = re.compile(r"<!-- changelog(?: (\d+))? -->")
REPO_URL = "https://github.com/StefCoene/xymon-docs-preview/commit/"


def _changelog(base, limit):
    """Commits of this site's own repository, newest first, as a Markdown table."""
    fmt = "%H%x09%cs%x09%s"
    args = ["git", "-C", base, "log", f"--format={fmt}", "--no-merges"]
    if limit:
        args.append(f"-{limit}")
    try:
        out = subprocess.run(args, capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return "*Change history is not available in this build.*"
    rows = ["| Date | Change |", "|---|---|"]
    for line in out.splitlines():
        sha, date, subject = line.split("\t", 2)
        subject = subject.replace("|", "\\|")
        rows.append(f"| {date} | [{subject}]({REPO_URL}{sha}) |")
    return "\n".join(rows)


# Each icon is also a character, so its meaning survives copy/paste, plain text and screen readers.
# Image sets paint over it with CSS; the "text" icon set shows it. "*" marks a recent change.
GLYPH = {"green": "\u2713", "yellow": "\u25b2", "red": "\u2715", "purple": "\u25c6", "clear": "\u25cb", "blue": "\u25a0"}
# Text versions of the other files a Xymon skin has (see ICONS-IN-XYMON.md)
GLYPH_EXTRA = {"unknown": ("unknown", "?"), "arrow": ("neutral", "\u2192"), "zoom": ("neutral", "\u2295")}
DOT = re.compile(r'<span class="xm-dot (\w+)( recent)?"([^>]*)></span>')


def _glyphs(markdown):
    def repl(m):
        status, recent, attrs = m.groups()
        mark = '<span class="xm-r">*</span>' if recent else ""
        return f'<span class="xm-dot {status}{recent or ""}"{attrs}>{GLYPH.get(status, "?")}{mark}</span>'

    return DOT.sub(repl, markdown)


# The wiki links to manual pages in the source tree (docs/<page>.html.DIST on GitHub). Send readers
# to the published manual page instead.
DIST = re.compile(
    r"\[`?docs/([\w.-]+)\.html\.DIST`?\]"
    r"\(https://github\.com/xymon-monitoring/xymon/blob/[\w.-]+/docs/\1\.html\.DIST\)( on GitHub)?"
)


def _dist_links(markdown, src_uri):
    here = posixpath.dirname(src_uri) or "."
    return DIST.sub(
        lambda m: f"[read it in the manual]({posixpath.relpath(f'manual/dev/{m.group(1)}.html', here)})", markdown
    )


ICON_TABLE = "<!-- xymon-icon-table -->"
ICON_SETS = [  # (name, folder, extension, has its own -recent images, statuses it covers)
    ("classic", "", "gif", True, SEVERITY),
    ("watcher", "watcher/", "gif", True, SEVERITY),
    ("vector", "vector/", "svg", True, SEVERITY),
    ("accessible", "accessible/", "svg", True, SEVERITY),
    ("christmas", "christmas/", "gif", True, ["green", "yellow", "red"]),
    ("gifts", "gifts/", "gif", False, SEVERITY),
    ("baubles", "baubles/", "png", True, SEVERITY),
]
STATUS_ORDER = ["green", "yellow", "red", "purple", "clear"]


MOVING = ["yellow", "red", "purple"]


def _icon_table(prefix):
    """Every status x state x icon set, straight from the image files the site uses."""
    cols = [n for n, *_ in ICON_SETS] + ["text", "copied as"]
    head = "".join(f'<th data-col="{c}">{c}</th>' for c in cols)
    boxes = "".join(f'<label><input type="checkbox" value="{c}" checked> {c}</label>' for c in cols)
    out = ['<details class="xm-cols"><summary>Choose columns <span class="xm-cols-count"></span></summary><div>'
           f'{boxes}<button type="button" data-cols="all">all</button></div></details>',
           '<div class="xm-matrix-wrap"><table class="xm-icons">',
           f"<thead><tr><th>Status</th><th>State</th>{head}</tr></thead><tbody>"]
    for st in STATUS_ORDER:
        states = [(True, True, "recent, animated"), (True, False, "recent"),
                  (False, True, "normal, animated"), (False, False, "normal")]
        if st not in MOVING:  # green and clear: only Watcher's own recent animation moves
            states = [x for x in states if x[0] or not x[1]]
        for i, (recent, anim, label) in enumerate(states):
            row = [f'<td rowspan="{len(states)}" class="xm-st">{st}</td>' if i == 0 else "", f'<td class="xm-state">{label}</td>']
            for name, folder, ext, own_recent, covers in ICON_SETS:
                in_set = st in covers
                src_folder, src_ext = (folder, ext) if in_set else ("", "gif")
                classic = src_folder == ""
                note = "" if in_set else " (classic: not in this set)"
                fname = f"{st}-recent" if recent and (own_recent or classic) else st
                style = []
                if recent and in_set and not own_recent:
                    style.append("filter: drop-shadow(0 0 3px #fff6b0)")
                moves = st in MOVING
                if anim and classic and moves:
                    src_folder = "animated/"
                elif anim and name == "watcher":  # its own pulse: the animated -recent GIF
                    src_folder, fname = "watcher/animated/", f"{st}-recent"
                elif anim and moves and src_ext == "svg":
                    style.append(f"--xm-c: var(--xm-{st}); animation: xm-pulse 1.8s ease-in-out infinite")
                elif anim and moves:
                    style.append("animation: xm-blink 1.2s steps(1, end) infinite")
                css = f' style="{"; ".join(style)}"' if style else ""
                pix = ' class="pix"' if src_ext in ("gif", "png") else ""
                alt = f"{name}: {st}{', recent' if recent else ''}{', animated' if anim else ''}{note}"
                row.append(f'<td data-col="{name}"><img src="{prefix}images/status/{src_folder}{fname}.{src_ext}" width="16" height="16" '
                           f'alt="{alt}" title="{alt}"{pix}{css}></td>')
            mark = "<sup>*</sup>" if recent else ""
            blink = ' style="animation: xm-blink 1.2s steps(1, end) infinite"' if anim and st in MOVING else ""
            row.append(f'<td data-col="text"><span class="xm-glyph {st}"{blink}>{GLYPH[st]}{mark}</span></td>')
            row.append(f'<td data-col="copied as"><code>{GLYPH[st]}{'*' if recent else ''}</code></td>')
            out.append(f'<tr class="{"xm-first" if i == 0 else ""}">{"".join(row)}</tr>')
    out.append("</tbody></table></div>")
    return "\n".join(out)


SKIN_TABLE = "<!-- xymon-skin-table -->"
SKIN_FILES = (  # (file name without extension, what Xymon uses it for)
    [(f"{c}{r}", "") for c in ["green", "yellow", "red", "purple", "blue", "clear"] for r in ("", "-recent")]
    + [(f"{c}-ack", "acknowledged") for c in MOVING]
    + [("unknown", "no status known"), ("unknown-recent", "no status known, recent"),
       ("arrow", "event log: from \u2192 to"), ("zoom", "graphs: zoom")])


def _skin_glyph(fname):
    """The text version of one skin file: the status character, * for recent, (..) for acknowledged."""
    base, _, state = fname.partition("-")
    cls, ch = GLYPH_EXTRA.get(base, (base, GLYPH.get(base, "")))
    if state == "ack":
        return f'<span class="xm-glyph {cls} xm-ack" title="{fname}">({ch})</span>'
    mark = "<sup>*</sup>" if state == "recent" else ""
    return f'<span class="xm-glyph {cls}" title="{fname}">{ch}{mark}</span>'


def _skin_table(prefix, docs_dir):
    """Per set, which files a complete Xymon skin needs and which exist."""
    sets = [(n, f, e) for n, f, e, *_ in ICON_SETS]
    head = "".join(f"<th>{n}</th>" for n, *_ in sets) + "<th>text</th>"
    out = ['<div class="xm-matrix-wrap"><table class="xm-icons xm-skin">',
           f"<thead><tr><th>File</th>{head}</tr></thead><tbody>"]
    have = {n: 0 for n, *_ in sets}
    for fname, use in SKIN_FILES:
        label = f"<code>{fname}</code>" + (f' <span class="xm-use">{use}</span>' if use else "")
        row = [f'<td class="xm-state">{label}</td>']
        for name, folder, ext in sets:
            rel = f"images/status/{folder}{fname}.{ext}"
            if os.path.exists(os.path.join(docs_dir, rel)):
                have[name] += 1
                size = "" if fname in ("arrow", "zoom") else ' width="16" height="16"'
                pix = ' class="pix"' if ext in ("gif", "png") else ""
                row.append(f'<td><img src="{prefix}{rel}"{size} alt="{name}: {fname}" title="{name}: {fname}.{ext}"{pix}></td>')
            else:
                row.append(f'<td class="xm-missing" title="{name}: no {fname}.{ext}">\u2013</td>')
        row.append(f"<td>{_skin_glyph(fname)}</td>")
        out.append(f"<tr>{''.join(row)}</tr>")
    total = len(SKIN_FILES)
    foot = "".join(f'<td class="{"xm-complete" if have[n] == total else ""}">{have[n]}/{total}</td>' for n, *_ in sets)
    out.append(f'</tbody><tfoot><tr><td class="xm-state">files present</td>{foot}<td class="xm-complete">{total}/{total}</td></tr></tfoot></table></div>')
    return "\n".join(out)


def on_page_markdown(markdown, page, config, files):
    if ICON_TABLE in markdown:
        depth = page.file.url.count("/")
        markdown = markdown.replace(ICON_TABLE, _icon_table("../" * depth))
    if SKIN_TABLE in markdown:
        depth = page.file.url.count("/")
        markdown = markdown.replace(SKIN_TABLE, _skin_table("../" * depth, config["docs_dir"]))
    markdown = _fix_links(markdown, page.file.src_uri)
    markdown = _dist_links(markdown, page.file.src_uri)
    markdown = _glyphs(markdown)
    base = os.path.dirname(config.config_file_path)
    markdown = CHANGELOG.sub(lambda m: _changelog(base, int(m.group(1) or 0)), markdown)
    if PLACEHOLDER not in markdown:
        return markdown
    today = dt.date.today()
    table, counts, worst = _render(today)
    total = sum(v for k, v in counts.items() if k != "clear")
    summary = (
        f'<div class="xm-summary" data-worst="{worst}">'
        f"<span>{total} pages tracked</span>"
        + "".join(f'<span><span class="xm-dot {s}"></span>{counts[s]} {s}</span>' for s in SEVERITY[:4])
        + f"<span>built {today.isoformat()}</span></div>"
    )
    return _glyphs(markdown.replace(PLACEHOLDER, table).replace(SUMMARY, summary))
