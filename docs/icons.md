# Status icons

Every icon is a character as well as a picture: ✓ green, ▲ yellow, ✕ red, ◆ purple, ○ clear, followed by `*` when the source changed in the last 30 days. Copy the grid into a mail or a text file and the statuses come along; screen readers read them too. An icon set only changes how that character looks, so a new theme (like Henrik's Christmas set) is a few lines of CSS and some images.

Switch sets above the grid on the home page. Your choice is remembered in your browser. Icons do not blink, unless you turn on **Blink recent changes**. Then only recent changes move: the pixel sets blink, the Vector and Accessible sets pulse with a glow in the status colour.

## Every combination

Each row is a status in one state; each column an icon set. The last two columns show the text version: how the **text** set draws it, and what you get when you copy the grid into a mail or a text file. *Recent* means the source changed in the last 30 days; *blinking* is how a recent icon looks with **Blink recent changes** turned on.

<!-- xymon-icon-table -->

On this site, *recent* can only be green: yellow means the source is 5+ years old, and red means the page is missing.

## Who made them

| Set | Made by |
|---|---|
| Classic | Stef Coene. Pixel icons in the traditional Xymon style: symbols for a status, faces for a recent change. Shown without animation. |
| Vector | Stef Coene. Soft, rounded SVG versions of the classic shapes. |
| Accessible | Stef Coene. SVG; a distinct shape and symbol for each status, in colour-blind-safe colours (Okabe-Ito); a recent change is shown filled, an older one hollow. |
| Watcher | Steven Aiello (2007–2008), from the Xymonton add-on [sa_icons](https://wiki.xymonton.org/doku.php/addons:sa_icons). One shape per colour, so the grid also works for colour-blind readers. His [README](images/status/watcher/README.txt): "Use them as you like". |
| Christmas | Henrik Størner, the author of Xymon (2007), from [Christmas.zip](https://www.xymon.com/misc/Christmas.zip) on xymon.com: baubles in the status colour, and a tree, a poinsettia or a bell for a recent change, on a fir-branch background. The set has no purple or clear icons, so the classic ones show there. [Notes](images/status/christmas/README.txt). |
| Gifts | Steve Dobbs (2003), gift boxes made "to get my grinch self into the Christmas spirit", from [gifts.tar.gz](https://web.archive.org/web/20080726061802if_/http://www.deadcat.net/40/gifts.tar.gz) on deadcat.net. One box per colour; a recent change gets a glow. His [read.me](images/status/gifts/README.txt). |
| Text | No images: the Unicode characters themselves, coloured with CSS. They scale and align with the text around them. |
