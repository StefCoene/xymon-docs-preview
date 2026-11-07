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


def on_config(config):
    base = os.path.dirname(config.config_file_path)
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
        rel = posixpath.relpath(resolved, prefix.rstrip("/"))
        base = SOURCES[prefix][len("https://github.com"):]
        path = posixpath.normpath(base + rel)
        return f"](https://github.com{path}{'#' + anchor if anchor else ''})"

    return LINK.sub(repl, markdown)


def on_page_markdown(markdown, page, config, files):
    markdown = _fix_links(markdown, page.file.src_uri)
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
    return markdown.replace(PLACEHOLDER, table).replace(SUMMARY, summary)
