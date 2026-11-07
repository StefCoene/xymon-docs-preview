---
hide:
  - navigation
  - toc
---

# Xymon documentation

Xymon monitors hosts, network services and anything else you configure it to check. This site brings together the documentation from every Xymon repository and links to the community resources around it.

The grid below works like a Xymon status page. Each row is a topic, each column a type of documentation. Click an icon to open the page. The icon shows how current the source is.

<!-- xymon-summary -->

<div class="xm-toolbar" role="group" aria-label="Icon set">
  Icons:
  <button type="button" data-icons="classic" aria-pressed="true">classic</button>
  <button type="button" data-icons="watcher" aria-pressed="false">watcher</button>
  <button type="button" data-icons="vector" aria-pressed="false">vector</button>
  <button type="button" data-icons="accessible" aria-pressed="false">accessible</button>
  <button type="button" data-icons="text" aria-pressed="false">text</button>
  <button type="button" data-icons="christmas" aria-pressed="false">christmas</button>
  <button type="button" data-icons="gifts" aria-pressed="false">gifts</button>
  <span>· Animate:
  <button type="button" data-anim="off" aria-pressed="true">off</button>
  <button type="button" data-anim="on" aria-pressed="false">on</button></span>
</div>

<!-- xymon-matrix -->

<div class="xm-legend">
  <span><span class="xm-dot green"></span>current</span>
  <span><span class="xm-dot yellow"></span>source unchanged for 5+ years</span>
  <span><span class="xm-dot red"></span>missing</span>
  <span><span class="xm-dot purple"></span>external, not migrated</span>
  <span><span class="xm-dot clear"></span>not applicable</span>
  <span><span class="xm-dot green recent"></span>changed in the last 30 days (* in plain text)</span>
</div>

**About the icons.** The colours mean what they mean in Xymon: green is fine, yellow needs a look, red is missing. Pick the icon set you like above the grid: the classic Xymon icons, Steven Aiello's Watcher set, two SVG sets (one colour-blind safe), plain text, or Henrik's Christmas icons. Your choice is remembered. Nothing moves unless you turn on **Animate**. Then, as in Xymon, yellow, red and purple move. Each icon is also a character (✓ ▲ ✕ ◆ ○, with `*` for a recent change), so the statuses survive copy/paste. [All icon sets, every combination, and who made them](icons.md).

## Recent changes to this site

<!-- changelog 5 -->

[Full changelog](changelog.md)

## Where to start

| I want to… | Go to |
|---|---|
| Install a Xymon server | [Installing Xymon](manual/dev/install.html) · [Compile Xymon](guides/how-to-compile-xymon.md) |
| Monitor my first hosts | [Configuring Xymon](manual/dev/xymon-config.html) · [hosts.cfg(5)](manual/dev/manpages/man5/hosts.cfg.5.html) |
| Get alerts | [Setting up alerts](manual/dev/xymon-alerts.html) · [alerts.cfg(5)](manual/dev/manpages/man5/alerts.cfg.5.html) |
| Monitor Windows | [PowerShell client](clients/windows-powershell/index.md) |
| Install from a package | [Download](download.md) |
| Ask a question | [Mailing list](community.md#mailing-list) |
