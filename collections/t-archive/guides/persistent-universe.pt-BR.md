[English](persistent-universe.md) · **Português** · [Acervo](../README.pt-BR.md)

# Universo persistente

Protótipo de evolução contínua de um estado modal, com três canais de memória, checkpoint e leituras passivas. O pacote inclui o harness Python, um exemplo TriadLang, um teste de continuidade e os resultados salvos.

[Ler o relatório original](../reading/pasta%20sem%20t%C3%ADtulo/triad_universe_v0/README.md) · [Todos os arquivos](../files/persistent-universe.md)

![Universo persistente](../source/pasta%20sem%20t%C3%ADtulo/triad_universe_v0/outputs/01_modal_field_evolution.png)

As notas registram 1.000.000 de modos residentes e 64 ticks de 8 passos. O volume lógico N³=10¹⁸ é metadado da representação, não uma matriz densa desse tamanho. O runtime nativo completo `libtriad_rt.so` não veio no ZIP; a biblioteca presente é apenas um shim de carregamento para CUDA opcional. A continuidade registrada não foi reexecutada nesta organização.

[Notas da execução](../reading/pasta%20sem%20t%C3%ADtulo/triad_universe_v0/RUN_NOTES.md)

[Dependências e portabilidade](../provenance/dependencies.pt-BR.md)
