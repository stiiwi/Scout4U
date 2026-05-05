# Codex Handoff

## Aktuelles Thema
Workflow verbessern: kurze Übergabe von ChatGPT an Codex.

## Ziel
Codex soll pro Arbeitspaket schnell erkennen, worum es geht, welche Dateien relevant sind, was nicht geändert werden soll und wie geprüft wird.

## Aktueller Stand
- Scout4U ist ein früher Python-/HTML-Prototyp für einen smarten Reisebegleiter für Camper.
- Aktuelle Demo liegt in demo.html und wird über generate_demo_html.py erzeugt.
- Ergebniskarten zeigen Typ-Pills, feste Camper-Service-Reihe, kompakte Entscheidungszeile, Fakten und Inline-Details.
- Kernlogik liegt in scout4u_score.py.
- GitHub Pages nutzt demo.html.
- main ist aktuell sauber und synchron, sofern nicht anders im Chat genannt.

## Aufgabe
Diese Datei künftig vor neuen Codex-Arbeitspaketen aktualisieren, wenn der Kontext sonst zu lang würde.

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
- project_status.md
- backlog.md

## Standard-Tests
- python3 generate_demo_html.py
- python3 scout4u_score.py --self-test
- git diff --check
- git status --short

## Arbeitsregel
Codex soll Änderungen klein halten, relevante Dateien nennen, Tests ausführen und keine Folgeaufträge an sich selbst formulieren.
