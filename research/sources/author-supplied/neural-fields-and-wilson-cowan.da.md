<!-- Translation of: research/sources/author-supplied/neural-fields-and-wilson-cowan.md; source commit: 304d75ed6ff646d311fd9df8b4e2db0d4dee277a -->
<!-- convertido de grok_report-67.pdf -->

"Neuralt felt" er her Wilson-Cowan/Amari/Nunez-linjen: aktivitet som kontinuerlig funktion af det kortikale rum — ikke NeRF (radiansfelt). HORN sagde den rette sætning: lokal svingning og global bølge er samme objekt på to skalaer. Feltet er den kontinuerlige skala.

Objektet

I stedet for N neuroner et felt u(x, t): middelrate (eller potentiale) i punktet x i vævet, ved tiden t. Vekselvirkning er ikke én Wij per par: den er en rumlig kerne w(x, x′) (hvor meget stedet x′ trækker stedet x). Kanonisk form (Amari):

τ∂tu(x,t) = −u(x,t) + ∫ w(x,x′) S(u(x′,t)) dx′ + I(x,t)

S er sigmoiden (rate vs. input). Wilson-Cowan skiller E- og I-populationer:

τE∂tE = −E + S(wEE(KEE ∗ E) − wIE(KIE ∗ I) + P)
τI∂tI = −I + S(wEI(KEI ∗ E) − wII(KII ∗ I) + Q)

∗ er foldning i rummet. Den klassiske mexikanerhat — eksitation nært, inhibition fjernt — er et w som giver et stabilt bump (rumlig arbejdshukommelse), vandrende bølge eller Turingmønster, afhængigt af forstærkning.

Nunez: samme ånd bliver en hjernebølgeligning når den aksonale forsinkelse træder ind. Coombes m.fl.: det moderne felt er en generaliseret "hjernebølgeligning".

Hvad feltet gør som det punktvise RNN ikke viser

Standardrepertoire (Bressloff / Coombes, oversigter):

- vandrende fronter og pulser
- breathere (lokaliseret svingning)
- spiraler i 2D
- Turingmønstre (geometrisk hallucination af V1-typen)
- persistent bump (rumlig WM, hovedretning)

Refraktæriteten som Wilson-Cowan allerede lagde ind i 1972-modellen ændrer fysikken: et rent eksitatorisk net, som uden refraktæritet kun bærer fronter, begynder at bære en periodisk bølge.

Reynolds m.fl. (ScienceDaily / 2026-rammen, vågen visuel korteks): den vandrende bølge er ingen EEG-dekoration. Fire foreslåede funktioner — justere perceptionen i øjeblikket, omdanne det nyligt sensoriske til repræsentation, forudse det korte fremad, mønster-replay. En analogi de selv skriver: indlært statistik som genererer næste tilstand, "som en LLM genererer tekst." Her er generatoren bølgen i vævet, ikke tokenet.

Dette stemmer med krage-LFP (beta/gamma i NCL) og HORN (interferens = repræsentation): tre skalaer, ét sprog.

HORN som diskretisering af feltet

Singer/Effenberger, PNAS 2025, eksplicit: HORN med lokal konnektivitet + geometriske stimuli lærer en mexikanerhat-lignende kerne. Den graf er meshet til et felt hvis associerede kontinuum er en dæmpet bølgeligning. Supplementfilm: anden stimulus, anden bølgeretning og -form.

Altså:

- HORN | neuralt felt
- Rum: n knuder | kontinuerligt x ∈ Z
- Tid: Euler af 2. ordens ODE | integro-differentialligning / bølge
- Kerne: Whh (indlært) | w(x, x′) (pålagt eller fittet)
- Repræsentation: transient interferens | front, bump, spiral
- Ringparameter: aksonal forsinkelse, τ, E/I-forstærkning

At hæve n og lokalisere W er at gå fra HORN til feltet. At sænke feltet til et mesh af oscillatorer er HORN.

Fra kontinuum til den virkelige graf (målt hjerne)

Graph neural fields (PLoS / PMC): samme Wilson-Cowan, men domænet er ikke planet — det er konnektomet (DTI + MRI). Graflaplacian i stedet for den kontinuerlige. Fluktuation i ligevægt reproducerer hvile-fMRI's harmoniske spektrum og forudsiger funktionel konnektivitet. Deres appendiks: dæmpet bølge på den menneskelige graf.

Lavdimensionelt felt (Neuron 2025–26): SNN af N LNP-neuroner, N → ∞, bliver et felt vt(z) i kredsløbsrummet Z. Hvis embedding z er rang-D, kollapser feltet til et D-dimensionalt system — den rigorøse bro mellem "fuldt net" og "neuronal masse." Nature Neuroscience (sep 2026) løfter et enkelt RNN frem trænet på multiregion-optagelser (fisk, mus, primat, menneske) for at inferere strøm mellem regioner. Felt er her måleværktøj, ikke kun teori.

Hvad AI gjorde med ideen (uden at kalde den korteks)

Tre grene som navnet "neuralt felt" i dag blander — bedst ikke at blande:

1. Trænbart klassisk felt. Conv-RNN som lærer at emittere bølger i den skjulte tilstand (arXiv 2502.06034): bølgesekvensen bliver visuel repræsentation; effektivt receptivt felt vokser uden globalt U-Net; semantisk segmentering med færre parametre. Det er HORN/felt anvendt på syn.
2. Neural Field Turing Machine (arXiv 2509.03370): kontroller + hukommelse som kontinuerligt felt + hoveder som læser/skriver en lokal patch. O(N) per nabolag, Turingkomplet under begrænset fejl. Instanser: Rule 110, 2D-varme, inpainting. Felt som deriverbart rumligt bånd.
3. Implicitte neurale repræsentationer / NeRF / SiREN / Functa. "Neuralt felt" i grafik: et net som parametriserer f(x), farve eller SDF. CORDS, ENF, FGN (2026) tager dette til grafer ("grafen er et udvalg af et entropifelt"). Anden familie: ingen Wilson-Cowan-bølge; en kontinuerlig funktion i stedet for meshet.

Den som kommer fra HORN vil have grenene 1–2. Gren 3 deler kun navnet.

Hvorfor det findes (beregning, ikke poesi)

Felt/bølge løser hvad transformeren løser med global opmærksomhed, anderledes:

- lang integration med lokal vægt — bølgen bærer konteksten; kernen er kort; det effektive receptive felt er rejsetid;
- rumlig prior i hardware — mexikanerhat er WM; intet behov for at lære "hold et bump";
- samme sprog som LFP — det du måler i krage og V1 er feltet;
- skala: kontinuum eller konnektomgraf, ikke tæt N².

Pris: stabilitetsanalyse (Turing, Hopf i feltet) i stedet for "stabl ét lag til." Identificerbarhed: Cremers viste at en plan bølge i en ratemodel og i integrate-and-fire afbildes på hinanden, men kernen infereret fra bølgehastigheden afhænger af den mikroskopiske klasse. Måle hastighed ± læse anatomi uden model.

På chattens tråd

```text
interferens
visuel NCC
vandrende bølge / bump
uden lag
Y, w, delay
kerne w(x,x')
```

OpenMythos/RDT: sløjfe i lagtid. Felt/HORN: sløjfe i bølgens fysiske tid. J-space: workspace som interpreterbarhed finder i LLM. Felt: workspace som anatomien er (aktivitet blevet global i forbifarten). De er ikke Mythos. De er — du lokaliserer vægtene og lader knuden svinge; filmen som kommer ud er et felt. Neurale feltnæt er denne film skrevet [ulæseligt i den konverterede kilde] — meshet bagfra og frem.
