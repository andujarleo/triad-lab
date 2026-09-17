[Início](README.md) · [English](../en/getting-started.md) · **Português**

# Executar um experimento

## Preparar

Os comandos usam um shell POSIX, a partir da raiz do repositório. Use Python 3.10
ou posterior (os scripts usam anotações de tipos modernas). As dependências são
requisitos de instalação, não um lockfile recuperado do ambiente original.

```sh
git clone https://github.com/andujarleo/triad-lab.git
cd triad-lab
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-visualization.txt
```

`requirements.txt` contém NumPy, Matplotlib e Pillow. A lista de visualização
acrescenta SciPy e scikit-image. Bravais tem alternativas NumPy para funções do
SciPy; as isosuperfícies precisam de scikit-image. A presença dessas bibliotecas
pode mudar os gráficos disponíveis e a implementação auxiliar executada.

## Começar por um estado salvo

Gere cordas de densidade e de espectro sem executar a evolução 3D:

```sh
MPLBACKEND=Agg python en/bravais/bravais_strings.py bravais/final_state.npz
```

As saídas vão para `bravais_outputs_3d/`. O estado incluído não contém `psi_f`, por
isso o script pula as cordas de fase. Isso é esperado para esse arquivo. A caixa
é assumida como `L=32`; informe o tamanho real pela variável `L` para outro estado.

## Executar uma simulação

```sh
python entre/simulate_observer_observed_relations.py
```

O experimento base usa 6.000 passos RK4 com `DT=0.02`. Grava PNG, GIF, JSON e NPZ
em `entre/artifacts/`. Consulte os outros scripts no [catálogo](../../experiments/README.pt-BR.md).
As versões em inglês gravam em `en/entre/artifacts/`.

Para a evolução Bravais ou a varredura de caixas:

```sh
MPLBACKEND=Agg python bravais/bravais_puro_3d.py
MPLBACKEND=Agg python bravais/bravais_sweep_L.py
```

A evolução padrão tem 1.200 passos em uma grade `64³`. A varredura usa 800 passos
por caixa e chega a `96³`, com maior consumo de recursos. Ambas aceitam `STEPS`
pelo ambiente; uma execução mais curta é outra execução. Ambas inicializam
aleatoriamente, sem semente fixa. As figuras salvas podem ser lidas sem executar.

## Separar execuções

Os scripts usam nomes de saída fixos e podem sobrescrever arquivos gerados antes.
Após cada execução, mova sua pasta de saída para `runs/<experiment-id>/<run-id>/`
antes de iniciar outra. Preencha uma cópia de [run.json](../../templates/run.json)
com comando, commit, ambiente, parâmetros e resultado. `runs/` é ignorado pelo Git;
publique seletivamente um registro revisado na pasta do experimento.

Vários scripts históricos executam ao serem importados. Use-os como scripts;
importar um módulo não é uma forma inofensiva de listar opções.

## Conferir a preservação

```sh
shasum -a 256 -c docs/archive/SHA256SUMS
```

A verificação confere os arquivos incluídos, sem afirmar repetição exata de uma
execução histórica. Arrays, figuras e parâmetros dos scripts são o registro
disponível; registre versões de dependências e hardware em cada nova execução.
