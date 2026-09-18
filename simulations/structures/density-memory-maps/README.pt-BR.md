[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Estruturas](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Mapas de densidade e memória

Snapshots comparam densidade, memória, resíduo e potencial de memória antes e depois de uma entrada gaussiana em t=0,5. O alinhamento local relatado é transitório; o registro também o compara com o campo ao redor.

Registro histórico importado; esta organização não reexecutou a simulação.

[Ler a nota original](notes/original-record.md) · [Todos os arquivos](FILES.md)

[Script preservado](code/simulate_density_memory_maps.py) · [Dependências e portabilidade](../../../provenance/t-archive/dependencies.pt-BR.md)

![Figura original do run](results/figures/mapa-0p000.png)


## Auditoria da execução

**Termos conjuntos documentados.** A atualização standalone fornecida documenta os termos conjuntos e três modos de memória com FDT ativo. O runner evolui novamente o caso do bolso plantado e registra mapas de densidade/memória; não é só leitor de imagens.

[Condições e contrastes registrados](../../../docs/pt-BR/execution-audit.md#study-t-39) · [simulate_density_memory_maps.py](code/simulate_density_memory_maps.py#L11) · [simulate_density_memory_maps.py](code/simulate_density_memory_maps.py#L43) · [simulate_density_memory_maps.py](code/simulate_density_memory_maps.py#L140)

## Material disponível

43 arquivos associados à ficha: 1 `.csv`, 1 `.json`, 1 `.md`, 40 `.png`.

[Cronologia](../../../docs/pt-BR/topics/timeline.md) · [← 38](../two-pockets/README.pt-BR.md)

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

Os arquivos mantêm a implementação e as condições registradas. Consulte a [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português) para as diferenças documentadas e o registro de dependências abaixo antes de preparar uma nova execução.

[Dependências e entradas ausentes](../../../provenance/t-archive/dependencies.pt-BR.md)

## Notas da implementação

Alguns protocolos arquivados acrescentam uma entrada durante a evolução: os estudos de bolsos inserem campos gaussianos no instante declarado `T_PLANT=0.5`; o script de impacto aplica uma perturbação declarada no pico do campo. Leia essas operações como intervenções registradas, não apenas condições iniciais nem automaticamente como calibração posterior ao resultado. [Fonte, linha 515](../a-pocket-in-the-field/code/simulate_field_pocket.py) · [Fonte deste estudo, linha 163](code/simulate_density_memory_maps.py).

[Auditoria estática completa e referências das fontes](../../../docs/maintenance/author-rules-audit.md).
