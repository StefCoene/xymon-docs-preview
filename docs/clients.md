# Clients

A Xymon client runs on each monitored host and reports to the server. Pick the one for your platform.

| Platform | Client | Documentation |
|---|---|---|
| Unix, Linux, BSD, macOS | Built-in client from the Xymon source tree | [Client / server communication](guides/client-server-communication.md) · [xymonclient.cfg(5)](manual/dev/manpages/man5/xymonclient.cfg.5.html) · [client-local.cfg(5)](manual/dev/manpages/man5/client-local.cfg.5.html) |
| Windows | PowerShell client (`xymon-client-windows-powershell`) | [PowerShell client](clients/windows-powershell/index.md) |
| Windows | MrBig | [xymon-mrbig/MrBig](https://github.com/xymon-mrbig/MrBig) |
| Any (Go) | go-xymon-client | [ArthurHlt/go-xymon-client](https://github.com/ArthurHlt/go-xymon-client) |
| Any (Python) | pyxymon, python-xymon | [madrisan/pyxymon](https://github.com/madrisan/pyxymon) · [skurfer/python-xymon](https://github.com/skurfer/python-xymon) |
| Network devices | Devmon (SNMP) | [bonomani/devmon](https://github.com/bonomani/devmon) |
| Any Unix, no install | xymon-rclient (over SSH) | [tools.rebel-it.com.au/xymon-rclient](https://tools.rebel-it.com.au/xymon-rclient/) |
| pfSense | Xymon client from the CLI | [Netgate forum](https://forum.netgate.com/topic/142506/how-to-setup-xymon-client-via-cli/1) |
