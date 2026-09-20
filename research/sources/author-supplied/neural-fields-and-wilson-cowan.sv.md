<!-- Translation of: research/sources/author-supplied/neural-fields-and-wilson-cowan.md; source commit: 304d75ed6ff646d311fd9df8b4e2db0d4dee277a -->
<!-- convertido de grok_report-67.pdf -->

"Neuralt fält" är här Wilson-Cowan/Amari/Nunez-linjen: aktivitet som kontinuerlig funktion av det kortikala rummet — inte NeRF ( radiansfält). HORN sade den rätta meningen: lokal svängning och global våg är samma objekt på två skalor. Fältet är den kontinuerliga skalan.

Objektet

I stället för N neuroner ett fält u(x, t): medelhastighet (eller potential) i punkten x i vävnaden, vid tiden t. Växelverkan är inte ett Wij per par: den är en rumslig kärna w(x, x′) (hur mycket stället x′ drar stället x). Kanonisk form (Amari):

τ∂tu(x,t) = −u(x,t) + ∫ w(x,x′) S(u(x′,t)) dx′ + I(x,t)

S är sigmoiden (hastighet vs. input). Wilson-Cowan separerar E- och I-populationer:

τE∂tE = −E + S(wEE(KEE ∗ E) − wIE(KIE ∗ I) + P)
τI∂tI = −I + S(wEI(KEI ∗ E) − wII(KII ∗ I) + Q)

∗ är faltning i rummet. Den klassiska mexikanska hatten — excitation nära, inhibition långt borta — är ett w som ger en stabil bump (spatialt arbetsminne), vandrande våg eller Turingmönster, beroende på förstärkning.

Nunez: samma anda blir en hjärnvågsekvation när den axonala fördröjningen träder in. Coombes m.fl.: det moderna fältet är en generaliserad "hjärnvågsekvation".

Vad fältet gör som det punkta RNN inte visar

Standardrepertoar (Bressloff / Coombes, översikter):

- vandrande fronter och pulser
- breathers (lokaliserad svängning)
- spiraler i 2D
- Turingmönster (geometrisk hallucination av V1-typ)
- persistent bump (spatialt WM, huvudriktning)

Refraktäriteten som Wilson-Cowan redan lade in i 1972 års modell ändrar fysiken: ett rent excitatoriskt nät, som utan refraktäritet bara bär fronter, börjar bära en periodisk våg.

Reynolds m.fl. (ScienceDaily / 2026 års ramverk, vaken visuell kortex): den vandrande vågen är ingen EEG-dekoration. Fyra föreslagna funktioner — justera perceptionen i ögonblicket, omvandla det nyligen sensoriska till representation, förutse den korta sikten, mönster-replay. En analogi de själva skriver: inlärd statistik som genererar nästa tillstånd, "som en LLM genererar text." Här är generatorn vågen i vävnaden, inte token.

Detta stämmer med kråk-LFP (beta/gamma i NCL) och HORN (interferens = representation): tre skalor, ett språk.

HORN som diskretisering av fältet

Singer/Effenberger, PNAS 2025, explicit: HORN med lokal konnektivitet + geometriska stimuli lär en mexikansk-hatt-lik kärna. Den grafen är meshen hos ett fält vars associerade kontinuum är en dämpad vågekvation. Supplementsfilmer: annan stimulus, annan vågriktning och -form.

Alltså:

- HORN | neuralt fält
- Rum: n noder | kontinuerligt x ∈ Z
- Tid: Euler av 2:a ordningens ODE | integro-differentialekvation / våg
- Kärna: Whh (inlärd) | w(x, x′) (pålagd eller fittad)
- Representation: transient interferens | front, bump, spiral
- Ringparameter: axonal fördröjning, τ, E/I-förstärkning

Att höja n och lokalisera W är att gå från HORN till fältet. Att sänka fältet till en mesh av oscillatorer är HORN.

Från kontinuum till den verkliga grafen (uppmätt hjärna)

Graph neural fields (PLoS / PMC): samma Wilson-Cowan, men domänen är inte planet — den är konnektomet (DTI + MRI). Graflaplacian i stället för den kontinuerliga. Fluktuation i jämvikt reproducerar vilofMRT:s harmoniska spektrum och förutser funktionell konnektivitet. Deras appendix: dämpad våg på den mänskliga grafen.

Lågdimensionellt fält (Neuron 2025–26): SNN av N LNP-neuroner, N → ∞, blir ett fält vt(z) i kretsrummet Z. Om inbäddningen z är rang-D kollapsar fältet till ett D-dimensionellt system — den rigorösa bron mellan "fullt nät" och "neural massa." Nature Neuroscience (sep 2026) lyfter ett enda RNN tränat på multiareainspelningar (fisk, mus, primat, människa) för att inferera ström mellan regioner. Fält är här mätverktyg, inte bara teori.

Vad AI gjorde med idén (utan att kalla den kortex)

Tre grenar som namnet "neuralt fält" i dag blandar — bäst att inte blanda:

1. Träningsbart klassiskt fält. Conv-RNN som lär sig att emittera vågor i det dolda tillståndet (arXiv 2502.06034): vågsekvensen blir visuell representation; effektivt receptivt fält växer utan globalt U-Net; semantisk segmentering med färre parametrar. Det är HORN/fält tillämpat på seende.
2. Neural Field Turing Machine (arXiv 2509.03370): kontroller + minne som kontinuerligt fält + huvuden som läser/skriver en lokal patch. O(N) per grannskap, Turingkomplett under begränsat fel. Instanser: Rule 110, 2D-värme, inpainting. Fält som deriverbart spatialt band.
3. Implicita neurala representationer / NeRF / SiREN / Functa. "Neuralt fält" i grafik: ett nät som parametriserar f(x), färg eller SDF. CORDS, ENF, FGN (2026) tar detta till grafer ("grafen är ett sampel av ett entropifält"). Annan familj: ingen Wilson-Cowan-våg; en kontinuerlig funktion i stället för meshen.

Den som kommer från HORN vill ha grenarna 1–2. Gren 3 delar bara namnet.

Varför det finns (beräkning, inte poesi)

Fält/våg löser vad transformern löser med global attention, annorlunda:

- lång integration med lokal vikt — vågen bär kontexten; kärnan är kort; det effektiva receptiva fältet är restid;
- spatial prior i hårdvara — mexikansk hatt är WM; inget behov att lära "håll en bump";
- samma språk som LFP — det du mäter i kråka och V1 är fältet;
- skala: kontinuum eller konnektomgraf, inte tätt N².

Kostnad: stabilitetsanalys (Turing, Hopf i fältet) i stället för "stapla ett lager till." Identifierbarhet: Cremers visade att en plan våg i en hastighetsmodell och i integrate-and-fire avbildas på varandra, men kärnan infererad ur våghastigheten beror på den mikroskopiska klassen. Mäta hastighet ± läsa anatomi utan modell.

På chattens tråd

```text
interferens
visuell NCC
vandrande våg / bump
utan lager
Y, w, delay
kärna w(x,x')
```

OpenMythos/RDT: slinga i lagertid. Fält/HORN: slinga i vågens fysikaliska tid. J-space: workspace som interpreterbarhet finner i LLM. Fält: workspace som anatomin är (aktivitet bliven global i förbigåendet). De är inte Mythos. De är — du lokaliserar vikterna och låter noden svänga; filmen som kommer ut är ett fält. Neurala fältnät är denna film skriven [oläsligt i den konverterade källan] — meshen bakifrån och fram.
