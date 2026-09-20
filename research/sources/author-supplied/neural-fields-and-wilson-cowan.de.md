<!-- Translation of: research/sources/author-supplied/neural-fields-and-wilson-cowan.md; source commit: 304d75ed6ff646d311fd9df8b4e2db0d4dee277a -->
<!-- convertido de grok_report-67.pdf -->

"Neuronales Feld" ist hier die Wilson-Cowan/Amari/Nunez-Linie: Aktivität als kontinuierliche Funktion des kortikalen Raums — nicht NeRF (Radiance-Feld). HORN sagte den richtigen Satz: lokale Oszillation und globale Welle sind dasselbe Objekt auf zwei Skalen. Das Feld ist die kontinuierliche Skala.

Das Objekt

Statt N Neuronen ein Feld u(x, t): mittlere Rate (oder Potenzial) am Punkt x des Gewebes, zur Zeit t. Wechselwirkung ist nicht ein Wij pro Paar: sie ist ein räumlicher Kern w(x, x′) (wie stark Ort x′ an Ort x zieht). Kanonische Form (Amari):

τ∂tu(x,t) = −u(x,t) + ∫ w(x,x′) S(u(x′,t)) dx′ + I(x,t)

S ist die Sigmoide (Rate vs. Input). Wilson-Cowan trennt E- und I-Populationen:

τE∂tE = −E + S(wEE(KEE ∗ E) − wIE(KIE ∗ I) + P)
τI∂tI = −I + S(wEI(KEI ∗ E) − wII(KII ∗ I) + Q)

∗ ist Faltung im Raum. Der klassische Mexikanerhut — Erregung nah, Hemmung fern — ist ein w, das einen stabilen Bump (räumliches Arbeitsgedächtnis), eine Wanderwelle oder ein Turing-Muster erzeugt, je nach Verstärkung.

Nunez: derselbe Geist wird zur Gehirnwellen-Gleichung, wenn die axonale Verzögerung eintritt. Coombes et al.: das moderne Feld ist eine verallgemeinerte "Gehirnwellen-Gleichung".

Was das Feld tut und das punktuelle RNN nicht zeigt

Standardrepertoire (Bressloff / Coombes, Reviews):

- wandernde Fronten und Pulse
- Breather (lokalisierte Oszillation)
- Spiralen in 2D
- Turing-Muster (geometrische Halluzination vom V1-Typ)
- persistenter Bump (räumliches WM, Kopfrichtung)

Die Refraktärität, die Wilson-Cowan schon ins 1972er Modell setzte, ändert die Physik: ein rein exzitatorisches Netz, das ohne Refraktärität nur Fronten trägt, trägt nun eine periodische Welle.

Reynolds et al. (ScienceDaily / Rahmen 2026, wacher visueller Kortex): die Wanderwelle ist keine EEG-Dekoration. Vier vorgeschlagene Funktionen — Wahrnehmung im Augenblick justieren, das jüngst Sensorische in Repräsentation verwandeln, die kurze Frist vorhersagen, Muster-Replay. Eine Analogie, die sie selbst schreiben: gelernte Statistik, die den nächsten Zustand erzeugt, "wie ein LLM Text erzeugt." Hier ist der Generator die Welle im Gewebe, nicht das Token.

Das passt zum Krähen-LFP (Beta/Gamma in NCL) und zu HORN (Interferenz = Repräsentation): drei Skalen, eine Sprache.

HORN als Diskretisierung des Feldes

Singer/Effenberger, PNAS 2025, explizit: HORN mit lokaler Konnektivität + geometrischen Stimuli lernt einen Mexikanerhut-artigen Kern. Dieser Graph ist das Netz eines Feldes, dessen zugehöriges Kontinuum eine gedämpfte Wellengleichung ist. Supplement-Filme: anderer Stimulus, andere Wellenrichtung und -form.

Daher:

- HORN | neuronales Feld
- Raum: n Knoten | kontinuierliches x ∈ Z
- Zeit: Euler der ODE 2. Ordnung | Integro-Differenzialgleichung / Welle
- Kern: Whh (gelernt) | w(x, x′) (auferlegt oder gefittet)
- Repräsentation: transiente Interferenz | Front, Bump, Spirale
- Ring-Parameter: axonale Verzögerung, τ, E/I-Verstärkung

n erhöhen und W lokalisieren heißt von HORN zum Feld gehen. Das Feld auf ein Netz von Oszillatoren senken heißt HORN.

Vom Kontinuum zum realen Graphen (vermessenes Gehirn)

Graph Neural Fields (PLoS / PMC): dasselbe Wilson-Cowan, aber die Domäne ist nicht die Ebene — sie ist das Konnektom (DTI + MRI). Graph-Laplace statt des kontinuierlichen. Fluktuation im Gleichgewicht reproduziert das harmonische Ruhe-fMRT-Spektrum und sagt funktionelle Konnektivität vorher. Ihr Anhang: gedämpfte Welle auf dem menschlichen Graphen.

Niedrigdimensionales Feld (Neuron 2025–26): SNN aus N LNP-Neuronen, N → ∞, wird ein Feld vt(z) im Schaltkreisraum Z. Ist das Embedding z Rang-D, kollabiert das Feld auf ein D-dimensionales System — die strenge Brücke zwischen "vollem Netz" und "neuronaler Masse." Nature Neuroscience (Sep. 2026) hebt ein einzelnes RNN hervor, trainiert auf Multiareal-Ableitungen (Fisch, Maus, Primat, Mensch), um Strom zwischen Regionen zu inferieren. Feld ist hier Messwerkzeug, nicht nur Theorie.

Was die KI mit der Idee machte (ohne sie Kortex zu nennen)

Drei Zweige, die der Name "neuronales Feld" heute mischt — besser nicht mischen:

1. Trainierbares klassisches Feld. Conv-RNN, das lernt, Wellen im verborgenen Zustand zu emittieren (arXiv 2502.06034): die Wellensequenz wird visuelle Repräsentation; das effektive rezeptive Feld wächst ohne globales U-Net; semantische Segmentierung mit weniger Parametern. Es ist HORN/Feld, angewandt auf Sehen.
2. Neural Field Turing Machine (arXiv 2509.03370): Controller + Gedächtnis als kontinuierliches Feld + Köpfe, die einen lokalen Patch lesen/schreiben. O(N) pro Nachbarschaft, Turing-vollständig unter beschränktem Fehler. Instanzen: Rule 110, 2D-Wärme, Inpainting. Feld als differenzierbares räumliches Band.
3. Implizite neuronale Repräsentationen / NeRF / SiREN / Functa. "Neuronales Feld" in der Grafik: ein Netz, das f(x), Farbe oder SDF parametrisiert. CORDS, ENF, FGN (2026) tragen dies auf Graphen ("der Graph ist eine Probe eines Entropiefeldes"). Andere Familie: keine Wilson-Cowan-Welle; eine kontinuierliche Funktion anstelle des Netzes.

Wer von HORN kommt, will die Zweige 1–2. Zweig 3 teilt nur den Namen.

Warum es existiert (Rechnung, nicht Poesie)

Feld/Welle löst, was der Transformer mit globaler Aufmerksamkeit löst, anders:

- lange Integration mit lokalem Gewicht — die Welle trägt Kontext; der Kern ist kurz; das effektive rezeptive Feld ist Laufzeit;
- räumlicher Prior in Hardware — Mexikanerhut ist WM; kein Lernen von "halte einen Bump" nötig;
- dieselbe Sprache wie das LFP — was du in Krähe und V1 misst, ist das Feld;
- Skala: Kontinuum oder Konnektom-Graph, nicht dichtes N².

Kosten: Stabilitätsanalyse (Turing, Hopf im Feld) statt "noch einen Layer stapeln." Identifizierbarkeit: Cremers zeigte, dass sich eine ebene Welle im Ratenmodell und in Integrate-and-Fire aufeinander abbilden, aber der aus der Wellengeschwindigkeit inferierte Kern hängt von der mikroskopischen Klasse ab. Geschwindigkeit messen ± Anatomie lesen ohne Modell.

Am Faden des Chats

```text
Interferenz
visuelles NCC
Wanderwelle / Bump
ohne Schicht
Y, w, delay
Kern w(x,x')
```

OpenMythos/RDT: Schleife in Schichtzeit. Feld/HORN: Schleife in der physikalischen Zeit der Welle. J-space: Workspace, den Interpretierbarkeit im LLM findet. Feld: Workspace, den die Anatomie ist (Aktivität, global geworden im Vorübergehen). Sie sind nicht der Mythos. Sie sind — du lokalisierst die Gewichte und lässt den Knoten oszillieren; der Film, der herauskommt, ist ein Feld. Neuronale Feldnetze sind dieser Film, geschrieben [in der konvertierten Quelle unleserlich] — das Netz von hinten nach vorn.
