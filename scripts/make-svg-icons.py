"""Export the missing vector/accessible SVGs from dig-bollen (Stef Coene) and draw unknown, arrow, zoom.

Usage: python3 scripts/make-svg-icons.py docs/images/status   (needs a dig-bollen checkout, see DB)
"""
import re, sys
from pathlib import Path

DB = Path("/home/staf/claude/DIG-ADMIN/repos/dig-bollen/templates")
OUT = Path(sys.argv[1])  # docs/images/status
HEAD = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'

def symbols(path):
    return dict(re.findall(r'<symbol id="([^"]+)" viewBox="0 0 16 16">(.*?)</symbol>', path.read_text()))

def write(folder, name, body, w=16, h=16):
    (OUT / folder / f"{name}.svg").write_text(HEAD.format(w=w, h=h) + body + "</svg>\n")

# ---- vector: currentColor -> Xymon colour (dark theme, as the existing files)
VEC = {"blue": "#3a8df0", "yellow": "#f2d01e", "red": "#f03a2a", "purple": "#b04fe0"}
vs = symbols(DB / "_icons.html")
for name in ["blue", "blue-recent", "yellow-ack", "red-ack", "purple-ack"]:
    col = VEC[name.split("-")[0]]
    write("vector", name, vs["i-" + name].replace("currentColor", col))

# ---- accessible: CSS variables -> Okabe-Ito colours, dark-theme line colours (as the existing files)
ACC = {  # fill, line, glyph
    "blue": ("#0072B2", "#4DA3E0", "#fff"), "yellow": ("#F0E442", "#F0E442", "#1c1c28"),
    "red": ("#D55E00", "#F28A3C", "#fff"), "purple": ("#CC79A7", "#E59BC3", "#1c1c28"),
}
ACK = "#7d848c"
acs = symbols(DB / "_icons_toegankelijk.html")
for name in ["blue", "blue-recent", "yellow-ack", "red-ack", "purple-ack"]:
    f, l, g = ACC[name.split("-")[0]]
    body = acs["n-" + name].replace("var(--f)", f).replace("var(--l)", l).replace("var(--g)", g).replace("var(--ack)", ACK)
    write("accessible", name, body)

# ---- new: unknown (no status known), in the style of each set
GREY, GREY_L = "#a0a0a0", "#b0b5bb"
QMARK = '<path d="M6 6.1a2 2 0 1 1 2.9 1.8c-.6.3-.9.7-.9 1.4" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/><circle cx="8" cy="11.9" r="{r}" fill="{c}"/>'
# vector "older": outlined rounded square with a question mark (like red/blue)
write("vector", "unknown",
      f'<rect x="1.5" y="1.5" width="13" height="13" rx="3" fill="{GREY}" fill-opacity=".18" stroke="{GREY}" stroke-width="1.3" stroke-dasharray="2.4 1.6"/>'
      + QMARK.format(c=GREY, w=1.6, r=1))
# vector "recent": filled face like the other recents, puzzled (wavy mouth)
write("vector", "unknown-recent",
      f'<circle cx="8" cy="8" r="7" fill="{GREY}"/><circle cx="8" cy="8" r="7" fill="#fff" fill-opacity=".14"/>'
      '<circle fill="#1c1c28" fill-opacity=".78" cx="5.8" cy="6.6" r=".95"/><circle fill="#1c1c28" fill-opacity=".78" cx="10.2" cy="6.6" r=".95"/>'
      '<path fill="none" stroke="#1c1c28" stroke-opacity=".78" stroke-width="1.3" stroke-linecap="round" d="M5 11q1.5-1.4 3 0t3 0"/>')
# accessible: hexagon (a shape no status uses) with three dots = "no information"
HEX = "M8 1.3l5.8 3.35v6.7L8 14.7l-5.8-3.35v-6.7z"
DOTS = '<g style="fill:{c}"><circle cx="5" cy="8" r="1.1"/><circle cx="8" cy="8" r="1.1"/><circle cx="11" cy="8" r="1.1"/></g>'
write("accessible", "unknown",
      f'<g stroke-width="1.5" stroke-linejoin="round" stroke-dasharray="2.3 1.9" style="fill:#9aa0a6;fill-opacity:.14;stroke:{GREY_L}"><path d="{HEX}"/></g>'
      + DOTS.format(c=GREY_L))
write("accessible", "unknown-recent",
      f'<g stroke-width="1" stroke-linejoin="round" style="fill:#9aa0a6;stroke:#1c1c28;stroke-opacity:.45"><path d="{HEX}"/></g>'
      + DOTS.format(c="#1c1c28"))

# ---- new: arrow (event log, "from -> to", 21x15 as Xymon's arrow.gif) and zoom (graphs, 16x16)
def arrow(col, w):
    return (f'<path d="M2 7.5h14.5M12 3l4.8 4.5L12 12" fill="none" stroke="{col}" stroke-width="{w}" '
            'stroke-linecap="round" stroke-linejoin="round"/>')
def zoom(col, glass, w):
    return (f'<circle cx="6.6" cy="6.6" r="4.6" fill="{glass}" fill-opacity=".22" stroke="{col}" stroke-width="{w}"/>'
            f'<path d="M10.1 10.1l4.2 4.2" stroke="{col}" stroke-width="{w + .9}" stroke-linecap="round"/>'
            f'<path d="M4.6 6.6h4M6.6 4.6v4" stroke="{col}" stroke-width="{w - .2}" stroke-linecap="round"/>')
write("vector", "arrow", arrow("#7aa7f5", 1.8), 21, 15)
write("vector", "zoom", zoom("#c8d8ff", "#7aa7f5", 1.4))
write("accessible", "arrow", arrow("#e8e8e8", 2.4), 21, 15)
write("accessible", "zoom", zoom("#e8e8e8", "#4DA3E0", 1.8))
print("ok")
