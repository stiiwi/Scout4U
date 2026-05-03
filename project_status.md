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
- Hauptdatei: scout4u_score.py
- Self-Test funktioniert: `python3 scout4u_score.py --self-test` -> Self-Test OK

## Aktuelle Dateien

- scout4u_score.py
- generate_demo_html.py
- demo.html
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
- Profil V / Camper-Vera mit rainy zeigt aktuell Stellplätze, Camper-Services und Ausflüge / schöne Orte.
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

- `generate_demo_html.py` erzeugt `demo.html`.
- Der Generator nutzt bestehende Logik aus `scout4u_score.py`.
- Die HTML-Demo lädt keine externen Ressourcen.
- Die HTML-Demo enthält keine Debug-Score-Details.
- `demo.html` zeigt eine lokale Scout4U-Demo für Profil Camper-Vera, Wetter Regen und Radius 25 km.
- Inhalt: Camper-Vorschläge rund um Bern aus den Beispiel-CSV-Dateien.

## Aktuelle Visuelle Richtung

- Hauptsächlich Blau, mit freundlichem und ruhigem App-Look.
- Smartphone-App-Mockup mit schmalem Container.
- Kompakter blauer Header.
- Statistik-Karten.
- Segment-Leiste für Stellplätze / Services / Ausflüge.
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

## Bestätigter Stand

- Alte Bern-Testprofile A/B/C laufen.
- Camper-Testprofil V läuft.
- Gruppierte Ausgabe funktioniert.
- --show-filtered funktioniert.
- Self-Test OK.
- Camper-Demoausgabe ist grundsätzlich zeigbar.
- Scoring wurde bei der Ausgabe-Politur nicht neu gebaut.

## Offene Designfragen

- Sollen Experience-Orte und Camper-Service-Orte später auch intern getrennte Cutoffs bekommen?
- Soll Wetter für Service-Orte schwächer gewichtet werden?
- Wie sollen Preise modelliert werden: kostenlos, unbekannt, Tagespreis, Nachtpreis?
- Wann wechseln wir von der lokalen Demo zu einer echten App-Struktur?
- Mixed-Orte können aktuell in Camper-Services erscheinen, wenn sie Camper-Nutzen haben; das ist logisch, könnte aber später in Benennung/Anzeige schöner erklärt werden.
- Soll die HTML-Demo später responsive werden: Desktop breiter, Mobile app-artig?

## Empfohlener nächster Schritt

Als nächstes sollte nicht am Scoring gedreht werden. Sinnvoller nächster Schritt:

1. Aktuellen HTML-Demo-Stand als Meilenstein stehen lassen oder Demo-Daten weiter verfeinern.
2. Optional später responsive Layout einbauen: Desktop breiter, Mobile app-artig.
3. Noch keine echte Android-App bauen, erst das Demo-Gefühl weiter testen.
