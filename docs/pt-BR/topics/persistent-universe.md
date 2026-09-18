[English](../../en/topics/persistent-universe.md) · **Português** · [Acervo](../history.md)

# Universo persistente

Protótipo de evolução contínua de um estado modal, com três canais de memória, checkpoint e leituras passivas. O pacote inclui o harness Python, um exemplo TriadLang, um teste de continuidade e os resultados salvos.

[Ler o relatório original](../../../experiments/continuity/persistent-universe/notes/README.md) · [Todos os arquivos](../../../experiments/continuity/persistent-universe/FILES.md)

![Universo persistente](../../../experiments/continuity/persistent-universe/results/figures/modal-field-evolution.png)

As notas registram 1.000.000 de modos residentes e 64 ticks de 8 passos. O volume lógico N³=10¹⁸ é metadado da representação, não uma matriz densa desse tamanho. O runtime nativo completo `libtriad_rt.so` não veio no ZIP; a biblioteca presente é apenas um shim de carregamento para CUDA opcional. A continuidade registrada não foi reexecutada nesta organização.

[Notas da execução](../../../experiments/continuity/persistent-universe/notes/run-notes.md)

[Dependências e portabilidade](../../../provenance/t-archive/dependencies.pt-BR.md)
