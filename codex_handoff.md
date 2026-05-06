# Codex Handoff

## Aktuelles Thema
Scout4U vom Demo-Feinschliff in Richtung App-/Produkt-Fundament führen.

## Ziel
Codex soll pro Arbeitspaket schnell erkennen, worum es geht, welche Dateien relevant sind, was nicht geändert werden soll und wie geprüft wird.

## Aktueller Stand
- Scout4U ist ein früher Python-/HTML-Prototyp für einen smarten Reisebegleiter für Camper.
- Aktuelle Demo liegt in demo.html und wird über generate_demo_html.py erzeugt.
- Ergebniskarten zeigen Typ-Pills, feste Camper-Service-Reihe, kompakte Entscheidungszeile, Fakten und Inline-Details.
- Das Karten-Upgrade ist abgeschlossen und soll jetzt nicht weiter kleinteilig poliert werden.
- app_concept.md beschreibt Produktidee, V1-Zielgruppe, Hauptflüsse und bewusste Nicht-Ziele.
- data_model.md skizziert ein zukünftiges Ort-/POI-Datenmodell ohne Migration in JSON, Datenbank oder App-Architektur.
- Die Demo hat einen statischen Radius-Mock mit 25 km / 40 km; 25 km ist initial aktiv.
- Radius, Wetter und Kategorie-Filter sind als App-Flow kombinierbar, ohne GPS, Karte, API oder Datenbank.
- Die aktuelle Zeile „Heute sinnvoll: ...“ ist eine Uebergangsloesung; spaeter sollen Match-Gruende eher als Chips oder Signale in Karten erscheinen.
- Kernlogik liegt in scout4u_score.py.
- GitHub Pages nutzt demo.html.
- main ist aktuell sauber und synchron, sofern nicht anders im Chat genannt.

## Aufgabe
Nächster Fokus: Produktlogik im bestehenden statischen Prototyp weiter schärfen, bevor neue technische App-Strukturen entstehen.

## Nicht ändern
- Keine Projektlogik ohne expliziten Auftrag.
- Kein Scoring-Umbau ohne expliziten Auftrag.
- Keine CSV-Datenänderung ohne expliziten Auftrag.
- Keine API, Datenbank, Karte oder echte App ohne expliziten Auftrag.

## Relevante Dateien
- scout4u_score.py
- generate_demo_html.py
- demo.html
- pois_camper_test_sample.csv
- profiles_camper_test_sample.csv
- app_concept.md
- data_model.md
- project_status.md
- backlog.md

## Standard-Tests
- python3 generate_demo_html.py
- python3 scout4u_score.py --self-test
- git diff --check
- git status --short

## Arbeitsregel
Codex soll Änderungen klein halten, relevante Dateien nennen, Tests ausführen und keine Folgeaufträge an sich selbst formulieren.
