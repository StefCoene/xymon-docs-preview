---
hide:
  - navigation
  - toc
---

# Xymon documentation

Xymon monitors hosts, network services and anything else you configure it to check. This site brings together the documentation from every Xymon repository and links to the community resources around it.

The grid below works like a Xymon status page. Each row is a topic, each column a type of documentation. Click an icon to open the page. The icon shows how current the source is.

<!-- xymon-summary -->

<div class="xm-toolbar" role="group" aria-label="Matrix view">
  View:
  <button type="button" data-view="all" aria-pressed="true">all topics</button>
  <button type="button" data-view="problems" aria-pressed="false">non-green only</button>
  <span>· Version: <a href="manual/4.3/install.html">4.3</a> | <strong>dev</strong></span>
</div>
<div class="xm-toolbar" role="group" aria-label="Icon set">
  Icons:
  <button type="button" data-icons="classic" aria-pressed="true">classic</button>
  <button type="button" data-icons="watcher" aria-pressed="false">watcher</button>
</div>

<!-- xymon-matrix -->

<div class="xm-legend">
  <span><span class="xm-dot green"></span>current</span>
  <span><span class="xm-dot yellow"></span>source unchanged for 5+ years</span>
  <span><span class="xm-dot red"></span>missing</span>
  <span><span class="xm-dot purple"></span>external, not migrated</span>
  <span><span class="xm-dot clear"></span>not applicable</span>
  <span><span class="xm-dot green recent"></span>changed in the last 30 days</span>
</div>

## Where to start

| I want to… | Go to |
|---|---|
| Install a Xymon server | [Installing Xymon](manual/dev/install.html) · [Compile Xymon](guides/how-to-compile-xymon.md) |
| Monitor my first hosts | [Configuring Xymon](manual/dev/xymon-config.html) · [hosts.cfg(5)](manual/dev/manpages/man5/hosts.cfg.5.html) |
| Get alerts | [Setting up alerts](manual/dev/xymon-alerts.html) · [alerts.cfg(5)](manual/dev/manpages/man5/alerts.cfg.5.html) |
| Monitor Windows | [PowerShell client](clients/windows-powershell/index.md) |
| Install from a package | [Download](download.md) |
| Ask a question | [Mailing list](community.md#mailing-list) |
