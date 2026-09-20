<!-- Translation of: research/sources/author-supplied/neural-fields-and-wilson-cowan.md; source commit: 304d75ed6ff646d311fd9df8b4e2db0d4dee277a -->
<!-- convertido de grok_report-67.pdf -->

"Nevralt felt" er her Wilson-Cowan/Amari/Nunez-linjen: aktivitet som kontinuerlig funksjon av det kortikale rommet — ikke NeRF (radiansfelt). HORN sa den rette setningen: lokal svingning og global bølge er samme objekt på to skalaer. Feltet er den kontinuerlige skalaen.

Objektet

I stedet for N nevroner et felt u(x, t): midlere rate (eller potensial) i punktet x i vevet, ved tiden t. Vekselvirkning er ikke én Wij per par: den er en romlig kjerne w(x, x′) (hvor mye stedet x′ trekker stedet x). Kanonisk form (Amari):

τ∂tu(x,t) = −u(x,t) + ∫ w(x,x′) S(u(x′,t)) dx′ + I(x,t)

S er sigmoiden (rate vs. input). Wilson-Cowan skiller E- og I-populasjoner:

τE∂tE = −E + S(wEE(KEE ∗ E) − wIE(KIE ∗ I) + P)
τI∂tI = −I + S(wEI(KEI ∗ E) − wII(KII ∗ I) + Q)

∗ er folding i rommet. Den klassiske meksikanerhatten — eksitasjon nært, inhibisjon fjernt — er en w som gir en stabil bump (romlig arbeidsminne), vandrende bølge eller Turingmønster, avhengig av forsterkning.

Nunez: samme ånd blir en hjernebølgeligning når den aksonale forsinkelsen trer inn. Coombes m.fl.: det moderne feltet er en generalisert "hjernebølgeligning".

Hva feltet gjør som det punktvise RNN ikke viser

Standardrepertoar (Bressloff / Coombes, oversikter):

- vandrende fronter og pulser
- breathere (lokalisert svingning)
- spiraler i 2D
- Turingmønstre (geometrisk hallusinasjon av V1-typen)
- persistent bump (romlig WM, hoderetning)

Refraktæriteten som Wilson-Cowan allerede la inn i 1972-modellen endrer fysikken: et rent eksitatorisk nett, som uten refraktæritet bare bærer fronter, begynner å bære en periodisk bølge.

Reynolds m.fl. (ScienceDaily / 2026-rammeverket, våken visuell korteks): den vandrende bølgen er ingen EEG-dekorasjon. Fire foreslåtte funksjoner — justere persepsjonen i øyeblikket, omdanne det nylig sensoriske til representasjon, forutsi det korte framover, mønster-replay. En analogi de selv skriver: innlært statistikk som genererer neste tilstand, "som en LLM genererer tekst." Her er generatoren bølgen i vevet, ikke tokenet.

Dette stemmer med kråke-LFP (beta/gamma i NCL) og HORN (interferens = representasjon): tre skalaer, ett språk.

HORN som diskretisering av feltet

Singer/Effenberger, PNAS 2025, eksplisitt: HORN med lokal konnektivitet + geometriske stimuli lærer en meksikanerhatt-lignende kjerne. Den grafen er meshet til et felt hvis assosierte kontinuum er en dempet bølgeligning. Supplementfilmer: annen stimulus, annen bølgeretning og -form.

Altså:

- HORN | nevralt felt
- Rom: n noder | kontinuerlig x ∈ Z
- Tid: Euler av 2. ordens ODE | integro-differensialligning / bølge
- Kjerne: Whh (innlært) | w(x, x′) (pålagt eller fittet)
- Representasjon: transient interferens | front, bump, spiral
- Ringparameter: aksonal forsinkelse, τ, E/I-forsterkning

Å heve n og lokalisere W er å gå fra HORN til feltet. Å senke feltet til et mesh av oscillatorer er HORN.

Fra kontinuum til den virkelige grafen (målt hjerne)

Graph neural fields (PLoS / PMC): samme Wilson-Cowan, men domenet er ikke planet — det er konnektomet (DTI + MRI). Graflaplacian i stedet for den kontinuerlige. Fluktuasjon i likevekt reproduserer hvile-fMRIs harmoniske spektrum og forutsier funksjonell konnektivitet. Deres appendiks: dempet bølge på den menneskelige grafen.

Lavdimensjonalt felt (Neuron 2025–26): SNN av N LNP-nevroner, N → ∞, blir et felt vt(z) i kretsrommet Z. Hvis embedding z er rang-D, kollapser feltet til et D-dimensjonalt system — den rigorøse broen mellom "fullt nett" og "nevronal masse." Nature Neuroscience (sep 2026) løfter fram et enkelt RNN trent på multiområdeopptak (fisk, mus, primat, menneske) for å inferere strøm mellom regioner. Felt er her måleverktøy, ikke bare teori.

Hva KI gjorde med ideen (uten å kalle den korteks)

Tre grener som navnet "nevralt felt" i dag blander — best å ikke blande:

1. Trenbart klassisk felt. Conv-RNN som lærer å emittere bølger i den skjulte tilstanden (arXiv 2502.06034): bølgesekvensen blir visuell representasjon; effektivt reseptivt felt vokser uten globalt U-Net; semantisk segmentering med færre parametre. Det er HORN/felt anvendt på syn.
2. Neural Field Turing Machine (arXiv 2509.03370): kontroller + minne som kontinuerlig felt + hoder som leser/skriver en lokal patch. O(N) per nabolag, Turingkomplett under begrenset feil. Instanser: Rule 110, 2D-varme, inpainting. Felt som deriverbart romlig bånd.
3. Implisitte nevrale representasjoner / NeRF / SiREN / Functa. "Nevralt felt" i grafikk: et nett som parametriserer f(x), farge eller SDF. CORDS, ENF, FGN (2026) tar dette til grafer ("grafen er et utvalg av et entropifelt"). Annen familie: ingen Wilson-Cowan-bølge; en kontinuerlig funksjon i stedet for meshet.

Den som kommer fra HORN vil ha grenene 1–2. Gren 3 deler bare navnet.

Hvorfor det finnes (beregning, ikke poesi)

Felt/bølge løser hva transformeren løser med global oppmerksomhet, annerledes:

- lang integrasjon med lokal vekt — bølgen bærer konteksten; kjernen er kort; det effektive reseptive feltet er reisetid;
- romlig prior i hardware — meksikanerhatt er WM; intet behov for å lære "hold en bump";
- samme språk som LFP — det du måler i kråke og V1 er feltet;
- skala: kontinuum eller konnektomgraf, ikke tett N².

Kostnad: stabilitetsanalyse (Turing, Hopf i feltet) i stedet for "stable ett lag til." Identifiserbarhet: Cremers viste at en plan bølge i en ratemodell og i integrate-and-fire avbildes på hverandre, men kjernen inferert fra bølgehastigheten avhenger av den mikroskopiske klassen. Måle hastighet ± lese anatomi uten modell.

På chattens tråd

```text
interferens
visuell NCC
vandrende bølge / bump
uten lag
Y, w, delay
kjerne w(x,x')
```

OpenMythos/RDT: sløyfe i lagtid. Felt/HORN: sløyfe i bølgens fysiske tid. J-space: workspace som interpreterbarhet finner i LLM. Felt: workspace som anatomien er (aktivitet blitt global i forbifarten). De er ikke Mythos. De er — du lokaliserer vektene og lar noden svinge; filmen som kommer ut er et felt. Nevrale feltnett er denne filmen skrevet [uleselig i den konverterte kilden] — meshet bakfra og fram.
