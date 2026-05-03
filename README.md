# Scout4U

Scout4U ist ein früher lokaler Prototyp für eine spätere App-Idee. In V1 soll Scout4U ein smarter Reisebegleiter für Camper und Camping-Reisende werden: Er schlägt passende Stellplätze, Services und Ausflüge in der Umgebung vor, abhängig von Wetter, Entfernung und persönlichen Vorlieben.

## Positionierung

Scout4U ist nicht nur eine Stellplatz-App. Der erste Fokus liegt auf Camping- und Camper-Reisen, aber mit breiterem Nutzen:

- Übernachten / Stellplätze
- Versorgen / Services
- Erleben / Ausflüge

Die Natur-&-Aussicht-Demo ist künftig als Beispiel für Ausflüge vom Reise-/Campingort aus zu verstehen, nicht als Beweis für eine komplett offene Allgemein-App.

## Aktueller Stand

- Lokaler Python-CLI-Prototyp.
- Noch keine echte App.
- Keine API.
- Keine Datenbank.
- Keine Karte/GPS.
- CSV-Dateien dienen aktuell als Testdaten.
- HTML-Demos werden lokal erzeugt.

## Demos

- `demo.html`: Camper-Demo rund um Bern bei Regen mit Stellplätzen, Services und Ausflügen.
- `demo_ausflug.html`: Natur-&-Aussicht-Demo rund um Bern bei Sonne, verstanden als Ausflüge vom Reise-/Campingort aus.

Beide Dateien können lokal im Browser geöffnet werden.

## Lokale Nutzung

Self-Test:

```bash
python3 scout4u_score.py --self-test
```

HTML-Demos erzeugen:

```bash
python3 generate_demo_html.py
```

## Wichtige Dateien

- `scout4u_score.py`: Hauptlogik für CSV-Parsing, Scoring, Filterung und CLI-Ausgabe.
- `generate_demo_html.py`: Erzeugt die lokalen HTML-Demos aus den bestehenden CSV-Testdaten.
- `project_status.md`: Detaillierter aktueller Projektstand und offene Fragen.
- `scout4u_testlog.md`: Bisherige Testnotizen und fachliche Beobachtungen.
- CSV-Testdaten: Beispiel-POIs und Beispiel-Profile für Bern, Camper-Reisen und Ausflugsszenarien.

## Projektstatus

Für den detaillierten aktuellen Stand siehe `project_status.md`.
