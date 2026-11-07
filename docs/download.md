# Download

The current stable release is **4.3.31** (6 November 2026). Version 4.4 is in development; the first alpha is tagged `4.4.0-alpha1`.

## Source

| What | Where |
|---|---|
| Release 4.3.31 | [GitHub release `rel-4.3.31`](https://github.com/xymon-monitoring/xymon/releases/tag/rel-4.3.31) |
| Development (main) | [xymon-monitoring/xymon](https://github.com/xymon-monitoring/xymon) |
| Older releases | [SourceForge](https://sourceforge.net/projects/xymon/files/) |

## Packages

| Platform | Package | Notes |
|---|---|---|
| Debian / Ubuntu | [`xymon`, `xymon-client`](https://packages.debian.org/sid/xymon) | In the distribution archive |
| RHEL, Rocky, Alma, Fedora | [xymon-rpm](https://xymon-monitoring.github.io/xymon-rpm/) | Official packaging, still experimental |
| RHEL, Fedora, Amazon Linux | [Terabithia RPMs](https://terabithia.org/rpms/xymon/) | Unofficial, by J.C. Cleaver, with many patches |
| FreeBSD | [`net-mgmt/xymon-server`, `xymon-client`](https://www.freshports.org/net-mgmt/xymon-server/) | Ports and packages |
| NetBSD and others | [pkgsrc `net/xymon`](https://ftp.mirrorservice.org/pub/NetBSD/NetBSD-current/pkgsrc/net/xymon/index.html) | |
| macOS | [Homebrew tap](https://github.com/xymon-monitoring/homebrew-xymon) · MacPorts | Server and client |
| Containers | [deweysasser/docker-xymon](https://github.com/deweysasser/docker-xymon) | Community image, not official |
| Ansible | [ipr-cnrs/xymon](https://github.com/ipr-cnrs/xymon) · [BertRaeymaekers/ansible-xymon](https://github.com/BertRaeymaekers/ansible-xymon) | Community roles |
| Puppet | [dodevops/xymon](https://forge.puppet.com/modules/dodevops/xymon) · [gardouille/xymon](https://forge.puppet.com/gardouille/xymon) | Community modules |
| Chef | [xymon cookbook](https://supermarket.chef.io/cookbooks/xymon) | Old, version 0.1.0 |

## Which version does my distribution ship?

[Repology](https://repology.org/project/xymon/versions) tracks Xymon in about 40 package repositories. Most still ship 4.3.30; FreeBSD already has 4.3.31.
