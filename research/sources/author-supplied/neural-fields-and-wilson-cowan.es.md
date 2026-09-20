<!-- Translation of: research/sources/author-supplied/neural-fields-and-wilson-cowan.md; source commit: 304d75ed6ff646d311fd9df8b4e2db0d4dee277a -->
<!-- convertido de grok_report-67.pdf -->

"Campo neuronal" aquí es el linaje Wilson-Cowan/Amari/Nunez: actividad como función continua del espacio cortical — no NeRF (campo de radiancia). HORN dijo la frase correcta: oscilación local y onda global son el mismo objeto en dos escalas. El campo es la escala continua.

El objeto

En vez de N neuronas, un campo u(x, t): tasa media (o potencial) en el punto x del tejido, en el tiempo t. La interacción no es un Wij por par: es un núcleo espacial w(x, x′) (cuánto el sitio x′ tira del sitio x). Forma canónica (Amari):

τ∂tu(x,t) = −u(x,t) + ∫ w(x,x′) S(u(x′,t)) dx′ + I(x,t)

S es la sigmoide (tasa vs. entrada). Wilson-Cowan separa poblaciones E e I:

τE∂tE = −E + S(wEE(KEE ∗ E) − wIE(KIE ∗ I) + P)
τI∂tI = −I + S(wEI(KEI ∗ E) − wII(KII ∗ I) + Q)

∗ es convolución en el espacio. El sombrero mexicano clásico — excitación cerca, inhibición lejos — es un w que genera un bump estable (memoria de trabajo espacial), onda viajera o patrón de Turing, según la ganancia.

Nunez: el mismo espíritu se vuelve ecuación de onda cerebral cuando entra el retardo axonal. Coombes et al.: el campo moderno es una "ecuación de onda cerebral" generalizada.

Lo que el campo hace que la RNN puntual no muestra

Repertorio estándar (Bressloff / Coombes, revisiones):

- frentes y pulsos viajeros
- breathers (oscilación localizada)
- espirales en 2D
- patrones de Turing (alucinación geométrica tipo V1)
- bump persistente (WM espacial, dirección de la cabeza)

La refractariedad que Wilson-Cowan ya ponía en el modelo de 1972 cambia la física: una red solo excitatoria, que sin refractariedad solo lleva frentes, pasa a llevar una onda periódica.

Reynolds et al. (ScienceDaily / marco 2026, corteza visual despierta): la onda viajera no es decoración del EEG. Cuatro funciones propuestas — ajustar la percepción en el instante, transformar lo sensorial reciente en representación, predecir el corto plazo, replay de patrón. Una analogía que ellos mismos escriben: estadística aprendida que genera el próximo estado, "como un LLM genera texto". Aquí el generador es la onda en el tejido, no el token.

Esto casa con el LFP de cuervo (beta/gamma en NCL) y con HORN (interferencia = representación): tres escalas, un idioma.

HORN como discretización del campo

Singer/Effenberger, PNAS 2025, explícito: HORN con conectividad local + estímulos geométricos aprende un núcleo tipo sombrero mexicano. Ese grafo es la malla de un campo cuyo continuo asociado es una ecuación de onda amortiguada. Películas del suplemento: estímulo distinto, dirección y forma de onda distintas.

Por tanto:

- HORN | campo neuronal
- Espacio: n nodos | x ∈ Z continuo
- Tiempo: Euler de la ODE de 2º orden | ecuación integro-diferencial / onda
- Núcleo: Whh (aprendido) | w(x, x′) (impuesto o ajustado)
- Representación: interferencia transitoria | frente, bump, espiral
- Parámetro de ring: retardo axonal, τ, ganancia E/I

Subir n y localizar W es ir de HORN al campo. Bajar el campo a una malla de osciladores es HORN.

Del continuo al grafo real (cerebro medido)

Graph neural fields (PLoS / PMC): el mismo Wilson-Cowan, pero el dominio no es el plano — es el conectoma (DTI + MRI). Laplaciano del grafo en lugar del continuo. La fluctuación en el equilibrio reproduce el espectro armónico del fMRI de reposo y predice conectividad funcional. Su apéndice: onda amortiguada en el grafo humano.

Campo de baja dimensión (Neuron 2025–26): SNN de N neuronas LNP, N → ∞, se vuelve un campo vt(z) en el espacio de circuitos Z. Si el embedding z es de rango D, el campo colapsa a un sistema de D dimensiones — el puente riguroso entre "red completa" y "masa neuronal". Nature Neuroscience (sep 2026) destaca una RNN única entrenada en grabaciones multiarea (pez, ratón, primate, humano) para inferir corriente entre regiones. Campo aquí es herramienta de medida, no solo teoría.

Lo que la IA hizo con la idea (sin llamarla corteza)

Tres ramas que el nombre "campo neuronal" hoy mezcla — conviene no mezclar:

1. Campo clásico entrenable. Conv-RNN que aprende a emitir ondas en el estado escondido (arXiv 2502.06034): la secuencia de ondas se vuelve representación visual; el campo receptivo efectivo crece sin U-Net global; segmentación semántica con menos parámetros. Es HORN/campo aplicado a visión.
2. Neural Field Turing Machine (arXiv 2509.03370): controlador + memoria como campo continuo + cabezas que leen/escriben un parche local. O(N) por vecindad, Turing-completo bajo error acotado. Instancias: Rule 110, calor 2D, inpainting. Campo como cinta espacial diferenciable.
3. Representaciones neuronales implícitas / NeRF / SiREN / Functa. "Campo neuronal" en gráficos: una red que parametriza f(x), color o SDF. CORDS, ENF, FGN (2026) lo llevan a grafos ("el grafo es una muestra de un campo de entropía"). Familia distinta: no hay onda de Wilson-Cowan; hay función continua en lugar de la malla.

Quien viene de HORN quiere las ramas 1–2. La rama 3 solo comparte el nombre.

Por qué existe (computación, no poesía)

Campo/onda resuelve lo que el transformer resuelve con atención global, de otro modo:

- integración larga con peso local — la onda lleva el contexto; el núcleo es corto; el campo receptivo efectivo es el tiempo de viaje;
- prior espacial en el hardware — sombrero mexicano es WM; no hace falta aprender "guarda un bump";
- mismo idioma que el LFP — lo que mides en cuervo y V1 es el campo;
- escala: continuo o grafo de conectoma, no N² denso.

Costo: análisis de estabilidad (Turing, Hopf en el campo) en lugar de "apila una layer más". Identificabilidad: Cremers mostró que una onda plana en un modelo de tasa y en integrate-and-fire se mapean, pero el núcleo inferido de la velocidad de onda depende de la clase microscópica. Medir velocidad ± leer anatomía sin modelo.

En el hilo del chat

```text
interferencia
NCC visual
onda viajera / bump
sin lámina
Y, w, delay
kernel w(x,x')
```

OpenMythos/RDT: lazo en el tiempo de capa. Campo/HORN: lazo en el tiempo físico de la onda. J-space: workspace que la interpretabilidad encuentra en el LLM. Campo: workspace que la anatomía es (actividad vuelta global al pasar). No son el Mythos. Son — localizas los pesos y dejas oscilar el nodo; la película que sale es un campo. Las redes de campos neuronales son esta película escrita [ilegible en la fuente convertida] — la malla de atrás hacia adelante.
