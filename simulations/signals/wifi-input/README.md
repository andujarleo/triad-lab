[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Signals](../README.md) · [Glossary](../../../docs/en/glossary.md) · [Project rules](../../../docs/en/project-rules.md)

# Fields initialized from WiFi scans

**Can measured WiFi scans initialize a field?**

The script reads real measurements from wifi_scans.csv; that file was not supplied. This entry preserves an implementation, not a demonstrated run with WiFi measurements.



## Execution audit

> **TRIAD identity: NOT complete TRIAD — documented departure.**
>
> Point-to-point record: [English](../../../docs/en/triad-identity-audit.md#study-wifi-input) · [Português](../../../docs/pt-BR/triad-identity-audit.md#study-wifi-input) · [Español](../../../docs/es/triad-identity-audit.md#study-wifi-input) · [Deutsch](../../../docs/de/triad-identity-audit.md#study-wifi-input) · [Svenska](../../../docs/sv/triad-identity-audit.md#study-wifi-input) · [Norsk](../../../docs/no/triad-identity-audit.md#study-wifi-input) · [Dansk](../../../docs/da/triad-identity-audit.md#study-wifi-input) · [中文（简体）](../../../docs/zh-CN/triad-identity-audit.md#study-wifi-input)

**Implementation differs.** The supplied source uses a different kinetic sign/noise update and conditional state guards from the reference. The required WiFi measurements were not supplied; this entry does not document a demonstrated run with those measurements.

[Conditions and recorded contrasts](../../../docs/en/execution-audit.md#study-wifi-input) · [bravais_wifi.py](code/bravais_wifi.py#L148) · [bravais_wifi.py](code/bravais_wifi.py#L226)

## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)

The files retain their recorded implementation and conditions. Read the [implementation audit](../../../docs/maintenance/author-rules-audit.md) for documented differences and the dependency record below before preparing a new execution.

[Dependencies and missing inputs](../../../provenance/t-archive/dependencies.md)
