# Scout4U Projektstatus

## Kurzbeschreibung

Scout4U ist ein lokaler Python-CLI-Prototyp für eine spätere mobile App-Idee. Die App soll langfristig passende Orte in der Umgebung empfehlen. Für Version 1.0 ist Camper-Reisen ein wichtiger Fokus, aber Scout4U soll langfristig breiter bleiben.

## Produktkontext

- Erste echte Nutzerin ist meine Mutter.
- Sie hatte die ursprüngliche App-Idee.
- Ich möchte ihr später einen kleinen, cool aussehenden Prototyp zeigen.
- Sie reist viel mit dem Camper, besonders in England, Frankreich, Island, Spanien und Italien.
- Camper-Funktionen sind deshalb für V1.0 hoch priorisiert.

## Aktueller technischer Stand

- Noch keine App.
- Keine API.
- Keine Datenbank.
- Keine Karte.
- Lokales Python-CLI-Tool mit CSV-Dateien.
- Git-Repository auf Branch `main`.
- Privates GitHub-Repository: `stiiwi/Scout4U`.
- Hauptdatei: scout4u_score.py
- Self-Test funktioniert: `python3 scout4u_score.py --self-test` -> Self-Test OK
- `.gitignore` ignoriert `.claude/`, damit lokale Tool-Arbeitsdaten nicht ins Repo kommen.
- `README.md` wurde als kurze Projektübersicht erstellt.

## Git/GitHub-Stand

- Projekt ist jetzt ein Git-Repository.
- Repository ist privat auf GitHub unter `stiiwi/Scout4U` gesichert.
- Aktueller Branch: `main`.
- Wichtige Commits:
  - `Initial Scout4U prototype with CLI and HTML demo`
  - `Improve HTML demo tabs and fit labels`
  - `Add excursion HTML demo`

## Aktuelle Dateien

- scout4u_score.py
- generate_demo_html.py
- demo.html
- demo_ausflug.html
- README.md
- pois_bern_test_sample.csv
- profiles_test_sample.csv
- pois_camper_test_sample.csv
- profiles_camper_test_sample.csv
- scout4u_testlog.md
- project_status.md

## Implementierte Kernlogik

- Input: POI-CSV und Profile-CSV.
- Output: Empfehlungen plus optional gefilterte Orte.
- Wetter: sunny/rainy.
- distance_km kommt direkt aus CSV.
- hard_anti_tags sind harte Ausschlüsse.
- soft_anti_tags geben -3 pro Treffer.
- touristenfalle / tourist_trap ist globaler harter Ausschluss.
- Kein Score-Cap.
- Cutoff: Score >= 5.0.
- Erlebnis-Gate: mindestens 2 Erlebnis-Tags für reine Experience-POIs.
- Camper-Service-Orte überspringen das Erlebnis-Gate.

## POI-Typen

- experience
- camper_service
- mixed

## Camper-Service-Logik

- Optionale POI-Spalten: poi_type, services, price_chf, overnight_allowed.
- Optionale Profile-Spalte: needs.
- Service-Score:
  - +3 pro passendem Need
  - +2 für overnight_allowed=ja bei Stellplatz-/Overnight-Bedarf
  - +1 für kostenlos
- Service-Orte werden nach Nutzwert bewertet, nicht nach Erlebniswert.

## Gruppierte Ausgabe

Empfehlungen werden gerendert in:

- Stellplätze
- Camper-Services
- Ausflüge / schöne Orte

Priorität bei Mehrfachzuordnung:

1. Stellplätze
2. Camper-Services
3. Ausflüge / schöne Orte

## Demo-Ausgabe

- Die normale Ausgabe zeigt keine Debug-Score-Details mehr.
- Score-Details sind nur noch mit `--debug-score` sichtbar.
- Der Score heißt in der normalen Ausgabe jetzt "Passung".
- Interne Tags werden menschenlesbar angezeigt, z.B. Frischwasser, WC-Entsorgung und Camper-Stellplatz.
- `poi_type` wird menschenlesbar als Kategorie angezeigt, z.B. Camper-Service.
- Wetterzeilen enthalten keine technischen `(indoor ...)` Zusätze mehr.
- Der Abschlusshinweis ist freundlicher formuliert.
- Profil V / Camper-Reise mit rainy zeigt aktuell Stellplätze, Camper-Services und Ausflüge / schöne Orte.
- Die Ausgabe ist grundsätzlich zeigbar und nicht mehr debug-lastig.

## Demo-Daten

- `pois_camper_test_sample.csv` wurde um 8 Beispiel-POIs erweitert.
- Die Camper-Demo zeigt jetzt bis zu 10 Treffer.
- Enthalten sind mehrere Stellplätze, Camper-Services, ein Mixed-Ort und ein Ausflugsziel.
- Ziel ist eine bessere, glaubwürdigere Mutter-Demo.

## Designnotiz Für Spätere UI

- Hauptfarben sollen Blau / verschiedene Blautöne sein.
- Stilrichtung: freundlich, ruhig, klar, nicht technisch.

## HTML-Demo

- `generate_demo_html.py` erzeugt mit einem Aufruf beide HTML-Demos:

```bash
python3 generate_demo_html.py
```

- Der Generator nutzt bestehende Logik aus `scout4u_score.py`.
- `scout4u_score.py` wurde für die zweite Demo nicht geändert.
- Die CSV-Dateien wurden für die zweite Demo nicht geändert.
- Die HTML-Demos laden keine externen Ressourcen.
- Die HTML-Demos enthalten keine Debug-Score-Details.
- `demo.html` zeigt eine lokale Scout4U-Demo für Profil Camper-Reise, Wetter Regen und Radius 25 km.
- Inhalt: Camper-Vorschläge rund um Bern aus den Camper-Beispiel-CSV-Dateien.
- `demo.html` hat interaktive Tabs für Stellplätze, Services und Ausflüge.
- Passung wird nutzerfreundlich als Label angezeigt, z.B. Sehr gute Passung, Gute Passung oder Solide Option.
- Die Demos wurden für eine erste Präsentation an eine Nicht-Tech-Nutzerin vorbereitet.
- Die sichtbaren Profilnamen wurden neutralisiert:
  - Camper-Reise
  - Natur & Aussicht
- Beide Demos haben freundliche Intro-Sätze in Alltagssprache.
- Beide Demos verlinken gegenseitig aufeinander, um zu zeigen, dass Scout4U nicht nur Camper-Services abdecken soll.

## Zweite HTML-Demo

- `demo_ausflug.html` wurde ergänzt.
- Demo zeigt Natur & Aussicht rund um Bern.
- Nutzt Profil A / Natur & Aussicht, Wetter Sonne und Radius 50 km.
- Nutzt bestehende Bern-Testdaten aus `pois_bern_test_sample.csv` und `profiles_test_sample.csv`.
- Zeigt aktuell 4 Top-Tipps.
- Die sichtbare Warum-Zeile zeigt keine Gewichtungszahlen in Klammern mehr.
- Ziel: zeigen, dass Scout4U langfristig mehr kann als Camper-Services.

## Aktuelle Visuelle Richtung

- Hauptsächlich Blau, mit freundlichem und ruhigem App-Look.
- Smartphone-App-Mockup mit schmalem Container.
- Kompakter blauer Header.
- Statistik-Karten.
- Camper-Demo: Segment-Leiste für Stellplätze / Services / Ausflüge.
- Ausflugsdemo: einfache Top-Tipps-Ansicht ohne künstliche Tab-Leiste.
- Einspaltige App-Karten mit Chips für Fakten und Services.

## UI-Learning

- Die vorherige breite Variante wirkte auf Desktop gut.
- Die neue Smartphone-Mockup-Variante wirkt deutlich mehr wie eine spätere App.
- Langfristig sinnvoll: Desktop als breite Web-/Demo-Ansicht und Smartphone als app-artige einspaltige Ansicht.
- Das kann später über responsive CSS umgesetzt werden.

## Wichtige Testbefehle

```bash
python3 scout4u_score.py --self-test
```

```bash
python3 scout4u_score.py --pois pois_bern_test_sample.csv --profiles profiles_test_sample.csv --profile A --weather rainy --top 10 --show-filtered
```

```bash
python3 scout4u_score.py --pois pois_camper_test_sample.csv --profiles profiles_camper_test_sample.csv --profile V --weather rainy --top 10 --show-filtered
```

Optional mit Score-Details:

```bash
python3 scout4u_score.py --pois pois_camper_test_sample.csv --profiles profiles_camper_test_sample.csv --profile V --weather rainy --top 10 --show-filtered --debug-score
```

## Letzte geprüfte Tests

```bash
python3 scout4u_score.py --self-test
```

Ergebnis: Self-Test OK

```bash
python3 generate_demo_html.py
```

Ergebnis: `demo.html` und `demo_ausflug.html` erfolgreich erzeugt.

## Bestätigter Stand

- Alte Bern-Testprofile A/B/C laufen.
- Camper-Testprofil V läuft.
- Gruppierte Ausgabe funktioniert.
- --show-filtered funktioniert.
- Self-Test OK.
- Camper-Demoausgabe ist grundsätzlich zeigbar.
- HTML-Camper-Demo ist zeigbar und interaktiv.
- HTML-Ausflugsdemo ist als zweites Szenario ergänzt.
- Beide HTML-Demos sind für eine erste Nicht-Tech-Vorführung geglättet.
- Beide HTML-Demos verlinken dezent aufeinander.
- README.md ist vorhanden.
- Self-Test war zuletzt grün.
- Scoring wurde bei der Ausgabe-Politur nicht neu gebaut.

## Aktuelle Einschätzung

- Der aktuelle Stand ist ein guter Demo-Meilenstein.
- Noch keine echte App, keine API, keine Datenbank und keine Karte.
- Scout4U zeigt jetzt zwei Richtungen:
  - Camper-Nutzen für V1.0.
  - Natur-/Ausflugs-Empfehlungen als breiteres Langfristsignal.
- Nächste sinnvolle Schritte könnten sein:
  - README bei Bedarf später erweitern.
  - Kleine UI-Politur.
  - Demo-Profile schöner benennen.
  - Später responsive Desktop/Mobile weiterdenken.
  - Noch keine echte Android-App bauen.

## Offene Designfragen

- Sollen Experience-Orte und Camper-Service-Orte später auch intern getrennte Cutoffs bekommen?
- Soll Wetter für Service-Orte schwächer gewichtet werden?
- Wie sollen Preise modelliert werden: kostenlos, unbekannt, Tagespreis, Nachtpreis?
- Wann wechseln wir von der lokalen Demo zu einer echten App-Struktur?
- Mixed-Orte können aktuell in Camper-Services erscheinen, wenn sie Camper-Nutzen haben; das ist logisch, könnte aber später in Benennung/Anzeige schöner erklärt werden.
- Soll die HTML-Demo später responsive werden: Desktop breiter, Mobile app-artig?

## Empfohlener nächster Schritt

Als nächstes sollte nicht am Scoring gedreht werden. Sinnvoller nächster Schritt:

1. Aktuellen Demo-Stand als Meilenstein stehen lassen.
2. README ergänzen, damit der Projektstand schnell verständlich ist.
3. Optional kleine UI-Politur oder schönere Demo-Profilnamen.
4. Später responsive Layout einbauen: Desktop breiter, Mobile app-artig.
5. Noch keine echte Android-App bauen, erst das Demo-Gefühl weiter testen.
