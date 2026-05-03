# Scout4U Projektstatus

## Kurzbeschreibung

Scout4U ist ein lokaler Python-CLI-Prototyp für eine spätere mobile App-Idee. In V1 soll Scout4U zuerst ein smarter Reisebegleiter für Camper und Camping-Reisende werden: Er schlägt passende Stellplätze, Services und Ausflüge in der Umgebung vor, abhängig von Wetter, Entfernung und persönlichen Vorlieben.

Scout4U ist dabei nicht nur eine Stellplatz-App. Der Fokus liegt auf Camping- und Camper-Reisen, aber mit breiterem Nutzen:

- Übernachten / Stellplätze
- Versorgen / Services
- Erleben

## Produktkontext

- Erste echte Nutzerin ist meine Mutter.
- Sie hatte die ursprüngliche App-Idee.
- Ich möchte ihr später einen kleinen, cool aussehenden Prototyp zeigen.
- Sie reist viel mit dem Camper, besonders in England, Frankreich, Island, Spanien und Italien.
- Camper- und Camping-Reisende sind deshalb der erste V1-Fokus.
- Ausflüge bleiben wichtig, werden aber als Tipps vom Reise-/Campingort aus verstanden.

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

- `generate_demo_html.py` erzeugt mit einem Aufruf die lokale HTML-Demo:

```bash
python3 generate_demo_html.py
```

- Der Generator nutzt bestehende Logik aus `scout4u_score.py`.
- `scout4u_score.py` wurde für die Demo-Zusammenführung nicht geändert.
- Die CSV-Dateien wurden für die Demo-Zusammenführung nicht geändert.
- Die HTML-Demo lädt keine externen Ressourcen.
- Die HTML-Demo enthält keine Debug-Score-Details.
- `demo.html` zeigt eine lokale Scout4U-Demo für Camper-Reisen rund um Bern.
- Inhalt: Stellplätze und Services aus den Camper-Beispiel-CSV-Dateien sowie Erleben-Ausflüge vom Reise-/Campingort aus.
- Die oberen Kategorie-Kacheln filtern die drei Hauptbereiche:
  - Übernachten
  - Services
  - Erleben
- Passung wird nutzerfreundlich als Label angezeigt, z.B. Sehr gute Passung, Gute Passung oder Solide Option.
- Die Demo enthält eine Merkliste / Gemerkte Orte.
- Jede Karte hat eine aufklappbare "Warum passt das?"-Erklärung.
- Die Demo wurde für eine erste Präsentation an eine Nicht-Tech-Nutzerin vorbereitet.
- Die sichtbaren Profilnamen wurden neutralisiert.
- Die bisher separate Natur-&-Aussicht-Demo wurde in die Erleben-Kategorie der Hauptdemo integriert.
- Erleben wird als Ausflüge für trockene oder sonnige Zeitfenster vom Reise-/Campingort aus erklärt.

## Aktuelle Visuelle Richtung

- Hauptsächlich Blau, mit freundlichem und ruhigem App-Look.
- Smartphone-App-Mockup mit schmalem Container.
- Kompakter blauer Header.
- Statistik-Karten.
- Obere Kategorie-Kacheln für Übernachten / Services / Erleben.
- Einspaltige App-Karten mit Chips für Fakten und Services.
- Merkliste / Gemerkte Orte als einfache lokale Demo-Interaktion.
- Aufklappbare "Warum passt das?"-Erklärungen pro Karte.

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

Ergebnis: `demo.html` erfolgreich erzeugt.

## Bestätigter Stand

- Alte Bern-Testprofile A/B/C laufen.
- Camper-Testprofil V läuft.
- Gruppierte Ausgabe funktioniert.
- --show-filtered funktioniert.
- Self-Test OK.
- Camper-Demoausgabe ist grundsätzlich zeigbar.
- HTML-Camper-Demo ist zeigbar und interaktiv.
- Die Erleben-/Ausflugsinhalte sind in die Hauptdemo integriert.
- Die HTML-Demo ist für eine erste Nicht-Tech-Vorführung geglättet.
- Merkliste / Gemerkte Orte ist in der Demo vorhanden.
- Aufklappbare "Warum passt das?"-Erklärungen pro Karte sind vorhanden.
- README.md ist vorhanden.
- Self-Test war zuletzt grün.
- Scoring wurde bei der Ausgabe-Politur nicht neu gebaut.

## Aktuelle Einschätzung

- Der aktuelle Stand ist ein guter Demo-Meilenstein.
- Noch keine echte App, keine API, keine Datenbank und keine Karte.
- Scout4U ist für V1.0 auf Camping-/Camper-Reisen fokussiert:
  - Übernachten / Stellplätze.
  - Versorgen / Services.
- Scout4U ergänzt dazu Erleben mit Ausflügen vom Reise-/Campingort aus.
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
