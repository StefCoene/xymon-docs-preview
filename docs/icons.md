# Status icons

Every icon is a character as well as a picture: ✓ green, ▲ yellow, ✕ red, ◆ purple, ○ clear, followed by `*` when the source changed in the last 30 days. Copy the grid into a mail or a text file and the statuses come along; screen readers read them too. An icon set only changes how that character looks, so a new theme (like Henrik's Christmas set) is a few lines of CSS and some images.

Switch sets above the grid on the home page. Your choice is remembered in your browser. Nothing moves unless you turn on **Animate**. Then, as in Xymon, the problem colours move (yellow, red, purple); green and clear stay still, except where a set animates them itself (Watcher's recent icons pulse in every colour): the Classic and Watcher sets play their own animated GIFs, the other pixel sets blink, and the Vector and Accessible sets pulse with a glow in the status colour.

## Every combination

Each row is a status in one state; each column an icon set. The last two columns show the text version: how the **text** set draws it, and what you get when you copy the grid into a mail or a text file. *Recent* means the source changed in the last 30 days; *animated* is how the icon looks with **Animate** turned on.

<!-- xymon-icon-table -->

On this site, *recent* can only be green: yellow means the source is 5+ years old, and red means the page is missing.

## Who made them

| Set | Made by |
|---|---|
| Classic | The icons that ship with Xymon (`xymond/wwwfiles/gifs`), collected by Henrik Størner in 2004–2005 from free archives ([his README](https://github.com/xymon-monitoring/xymon/blob/main/xymond/wwwfiles/gifs/README)): green from the Big Sister `bigbro13` skin; red, yellow, purple and clear from the deadcat.net "animated-bb-icons" collection; the faces for a recent change from the deadcat "smile" set. Yellow, red and purple are animated; with **Animate** off this site shows one still frame of each. |
| Vector | Stef Coene. Soft, rounded SVG versions of the classic shapes. |
| Accessible | Stef Coene. SVG; a distinct shape and symbol for each status, in colour-blind-safe colours (Okabe-Ito); a recent change is shown filled, an older one hollow. |
| Watcher | Steven Aiello (2007–2008), from the Xymonton add-on [sa_icons](https://wiki.xymonton.org/doku.php/addons:sa_icons). One shape per colour; a recent change pulses (with **Animate** off, this site shows it still), so the grid also works for colour-blind readers. His [README](images/status/watcher/README.txt): "Use them as you like". |
| Christmas | Henrik Størner, the author of Xymon (2007), from [Christmas.zip](https://www.xymon.com/misc/Christmas.zip) on xymon.com: baubles in the status colour, and a tree, a poinsettia or a bell for a recent change, on a fir-branch background. The set has no purple or clear icons, so the classic ones show there. [Notes](images/status/christmas/README.txt). |
| Gifts | Steve Dobbs (2003), gift boxes made "to get my grinch self into the Christmas spirit", from [gifts.tar.gz](https://web.archive.org/web/20080726061802if_/http://www.deadcat.net/40/gifts.tar.gz) on deadcat.net. One box per colour; a recent change gets a glow. His [read.me](images/status/gifts/README.txt). |
| Baubles | Bruno Manzoni. Christmas baubles in all six status colours (blue included), 16×16 PNG; a gold sparkle marks a recent change. The only Christmas set with purple and clear. [Notes](images/status/baubles/README.txt). |
| Text | No images: the Unicode characters themselves, coloured with CSS. They scale and align with the text around them. |
