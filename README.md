# Scout4U

Scout4U ist ein früher lokaler Prototyp für eine spätere App-Idee. In V1 soll Scout4U ein smarter Reisebegleiter für Camper und Camping-Reisende werden: Er schlägt passende Stellplätze, Services und Ausflüge in der Umgebung vor, abhängig von Wetter, Entfernung und persönlichen Vorlieben.

## Positionierung

Scout4U ist nicht nur eine Stellplatz-App. Der erste Fokus liegt auf Camping- und Camper-Reisen, aber mit breiterem Nutzen:

- Übernachten / Stellplätze
- Versorgen / Services
- Erleben

Die Erleben-Kategorie zeigt Ausflüge vom Reise-/Campingort aus, nicht eine komplett offene Allgemein-App.

## Aktueller Stand

- Lokaler Python-CLI-Prototyp.
- Noch keine echte App.
- Keine API.
- Keine Datenbank.
- Keine Karte/GPS.
- CSV-Dateien dienen aktuell als Testdaten.
- Eine lokale HTML-Demo wird erzeugt.

## Demo

- `demo.html`: Camper-Demo rund um Bern mit Stellplätzen, Services und Ausflügen vom Reise-/Campingort aus.

Die Datei kann lokal im Browser geöffnet werden.

## Lokale Nutzung

Self-Test:

```bash
python3 scout4u_score.py --self-test
```

HTML-Demo erzeugen:

```bash
python3 generate_demo_html.py
```

## Wichtige Dateien

- `scout4u_score.py`: Hauptlogik für CSV-Parsing, Scoring, Filterung und CLI-Ausgabe.
- `generate_demo_html.py`: Erzeugt die lokale HTML-Demo aus den bestehenden CSV-Testdaten.
- `project_status.md`: Detaillierter aktueller Projektstand und offene Fragen.
- `scout4u_testlog.md`: Bisherige Testnotizen und fachliche Beobachtungen.
- CSV-Testdaten: Beispiel-POIs und Beispiel-Profile für Bern, Camper-Reisen und Ausflugsszenarien.

## Projektstatus

Für den detaillierten aktuellen Stand siehe `project_status.md`.
