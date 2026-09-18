[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Sinais](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Campos iniciados por leituras WiFi

**Leituras de WiFi podem iniciar um campo?**

O script lê medidas reais de wifi_scans.csv; esse arquivo não foi fornecido. A entrada preserva uma implementação, não uma execução demonstrada com medidas de WiFi.



## Auditoria da execução

**Implementação divergente.** A fonte fornecida usa sinal cinético/atualização de ruído e guards condicionais de estado diferentes da referência. As medidas WiFi necessárias não foram fornecidas; esta entrada não documenta uma execução demonstrada com essas medidas.

[Condições e contrastes registrados](../../../docs/pt-BR/execution-audit.md#study-wifi-input) · [bravais_wifi.py](code/bravais_wifi.py#L148) · [bravais_wifi.py](code/bravais_wifi.py#L226)

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

Os arquivos mantêm a implementação e as condições registradas. Consulte a [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português) para as diferenças documentadas e o registro de dependências abaixo antes de preparar uma nova execução.

[Dependências e entradas ausentes](../../../provenance/t-archive/dependencies.pt-BR.md)
