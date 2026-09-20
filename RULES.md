# RULES.md — triadlang

Regras normativas deste repositório. Valem para toda sessão, independente
de agente ou data. Em conflito: instrução direta de Leonardo > este
arquivo > AGENTS.md > padrões do ambiente.

## Idioma

Português por padrão. Código, identificadores e termos técnicos mantidos
no original.

## Resultado primeiro (skill `result-first`)

Carregue `.agents/skills/result-first/SKILL.md` no início do trabalho.
Resumo normativo, válido mesmo se a skill falhar ao carregar:

1. Turno de resultado: número/fato plano, condições em uma linha, parar.
2. Nenhuma ressalva, reinterpretação ou comparação externa liderando o
   resultado — para vitória, derrota e surpresa, o mesmo formato.
3. Explicação de mecanismo só com medição no mesmo turno e citação
   (arquivo:linha ou saída verbatim); sem isso, no máximo uma linha
   marcada HIPÓTESE, ou silêncio.
4. Escolha de tarefa ambígua: até 3 opções de uma linha, esperar a letra,
   executar. Nada de default silencioso nem pergunta aberta.
5. Aceitação seguida de parada é saída válida. Não fabricar trabalho.

## TRIAD

Carregue a skill `triad` quando o tema for TRIAD. A equação é imutável;
implementações e documentos têm revisão. Integral sempre: nenhum termo
desligado, zerado, congelado ou mockado para controle, teste, demo ou
benchmark. Benchmarks: o sistema é a equação — qualquer lado que a rode
é TRIAD; disputável é tarefa de resultado com métodos disjuntos.

## Preservação

Código, dados e resultados históricos não são apagados nem reescritos.
Leitura ou execução não autoriza reparo. Correção só no escopo
autorizado, com registro separado da execução anterior.

## Ambiente

Sandbox ou aprovação que bloqueia medição é verificação BLOQUEADA
precisando de decisão do autor — nunca negativo assentado. Medição
ordenada pode pedir escalação. Saída vazia vinda de negação não é
evidência de ausência.
