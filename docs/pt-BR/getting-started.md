[Lab](README.md) · [English](../en/getting-started.md) · **Português**

# Execute um estudo

Estes comandos examinam ou executam implementações históricas preservadas. Eles não certificam conformidade com a referência 1.1. Consulte o [histórico de versões](../reference/equation/README.md) e a configuração declarada de cada estudo antes de iniciar uma nova execução.

Os comandos usam um shell POSIX, a partir da raiz do repositório, e Python 3.10 ou mais recente. Os requisitos são uma base de instalação; não são um lockfile recuperado do ambiente original.

```sh
git clone https://github.com/andujarleo/triad-lab.git
cd triad-lab
git lfs install
git lfs pull
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-visualization.txt
python tools/check_repository.py
```

Instale Git LFS antes de usar `git lfs`. As figuras PNG podem ser lidas no GitHub; matrizes e animações usam LFS. `requirements.txt` inclui NumPy, Matplotlib e Pillow; a lista de visualização acrescenta SciPy e scikit-image. A presença dessas bibliotecas pode mudar o caminho de execução dos auxiliares e as figuras disponíveis.

## Comece por um estado salvo

```sh
MPLBACKEND=Agg python experiments/geometry/string-analysis/code/en/bravais_strings.py experiments/geometry/field-3d/results/data/final_state.npz
```

Esse comando lê o estado e escreve figuras em `bravais_outputs_3d/`, sem executar novamente a evolução do campo. O estado incluído não contém `psi_f`, então a seção de cordas de fase é ignorada. O script usa `L=32`; para outro estado, informe o tamanho real pela variável `L`.

## Execute os osciladores

```sh
python experiments/relations/observer/code/en/simulate_observer_observed_relations.py
```

São 6.000 passos RK4 com `DT=0.02`. As novas saídas ficam em `artifacts/` ao lado do script. A versão em português está em `code/pt-BR/` no mesmo estudo.

## Evolução 3D e varredura

```sh
MPLBACKEND=Agg python experiments/geometry/field-3d/code/en/bravais_pure_3d.py
MPLBACKEND=Agg python experiments/geometry/scale-sweep/code/en/bravais_sweep_L.py
```

A evolução usa por padrão 1.200 passos em uma grade 64³. A varredura usa 800 passos por caixa e chega a 96³, exigindo mais recursos. Ambos aceitam `STEPS` pelo ambiente, mas encurtar a execução cria outra comparação. A inicialização aleatória não fixa uma semente; os padrões não reconstituem exatamente o registro incluído.

## Separe cada execução

Scripts usam nomes fixos de saída e podem sobrescrever arquivos gerados. Antes da próxima execução, mova as novas saídas para `runs/<study-id>/<run-id>/`, que é ignorado pelo Git. Registre comando, diretório de trabalho, ambiente, parâmetros e hashes no modelo de execução. Não publique saídas novas por cima das antigas.

[Modelo de execução](../../templates/run.json) · [Dependências históricas](../../provenance/t-archive/dependencies.pt-BR.md)

Muitos scripts históricos executam ao importar e contêm caminhos antigos. Não os importe apenas para listar opções. Adaptações de caminhos ou dependências precisam de um registro próprio; a reorganização preservou o código numérico.
