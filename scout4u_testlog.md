# Scout4U Testlog

- Datum: 2026-05-02
- Projekt: Scout4U lokales Python-CLI-Score-Test-Tool

## Getestete Dateien

- scout4u_score.py
- pois_bern_test_sample.csv
- profiles_test_sample.csv

## Bestätigte Tests

- `python3 scout4u_score.py --self-test` -> Self-Test OK
- `python3 scout4u_score.py --help` -> Hilfe wird korrekt angezeigt
- Profil A rainy läuft erfolgreich
- Profil B rainy läuft erfolgreich
- Profil C rainy läuft erfolgreich

## Kurze fachliche Beobachtungen

- Beatushöhlen ist bei Profil A rainy Platz 1
- Zentrum Paul Klee ist bei Profil B und C rainy Platz 1
- Touristenfalle wird hart ausgeschlossen
- Stockhorn wird bei Profil B/C durch hard_anti_tag wanderung_schwer ausgeschlossen oder durch Radius gefiltert
- Café Bahnhof wird wegen zu wenigen Erlebnis-Tags ausgeschlossen
- Shoppyland bleibt unter Cutoff und wird nicht empfohlen

## Offene Designfragen

- Regenbewertung für reine Outdoor-Orte eventuell später nachschärfen
- Profil C / Städtetrip: Altstadt fällt bei Regen knapp unter Cutoff, später prüfen
- Cutoff 5.0 und Erlebnis-Gate später mit größeren Testdaten validieren

## Camper-Service-Erweiterung

### Neue Anforderung

- Entsorgungsstellen für WC / Chemietoilette im Camper
- Camper-Stellplätze mit Preis und Dienstleistungen
- öffentliche Toiletten

### Geänderte/erstellte Dateien

- scout4u_score.py geändert
- pois_camper_test_sample.csv erstellt
- profiles_camper_test_sample.csv erstellt

### Neue Modelllogik

- optionale POI-Spalten: poi_type, services, price_chf, overnight_allowed
- optionale Profile-Spalte: needs
- poi_type-Werte: experience, camper_service, mixed
- camper_service überspringt das Erlebnis-Gate
- mixed kann entweder über Erlebniswert oder Service-Nutzen empfohlen werden
- Service-Score: +3 pro passendem Need, +2 für overnight_allowed=ja bei Stellplatz-/Overnight-Bedarf, +1 für kostenlos
- kein Score-Cap bleibt bestehen

### Bestätigte Tests

- `python3 scout4u_score.py --self-test` -> Self-Test OK
- Camper-Testlauf rainy mit Profil V läuft erfolgreich
- Stellplatz Eichholz ist Platz 1
- Öffentliche Toilette Bahnhof wird empfohlen
- Camper-Service Wankdorf wird empfohlen
- Badestelle Wohlensee mit WC fällt unter Cutoff
- Hundewaschplatz Ost fällt unter Cutoff
- Gurten Panorama fällt unter Cutoff

### Offene Designfragen

- Sollen Experience-Orte und Camper-Service-Orte später getrennte Ergebnislisten haben?
- Soll Wetter für Service-Orte schwächer gewichtet werden?
- Brauchen Service-Orte einen eigenen Cutoff?
- Wie sollen Preise semantisch unterschieden werden: kostenlos, unbekannt, Tagespreis, Nachtpreis?

## Gruppierte Ausgabe

### Ziel

- Empfehlungen werden nicht mehr nur als eine gemeinsame Liste ausgegeben.
- Für Version 1.0 ist Camper ein wichtiger Fokus, aber Scout4U bleibt langfristig breiter.
- Deshalb werden Stellplätze, Camper-Services und Ausflüge getrennt angezeigt.

### Geänderte Datei

- scout4u_score.py

### Neue Ausgabegruppen

- Stellplätze
- Camper-Services
- Ausflüge / schöne Orte

### Gruppierungslogik

- Stellplätze: camper_stellplatz, stellplatz oder overnight_allowed=ja
- Camper-Services: wc_entsorgung, chemietoilette, toilette, oeffentliche_toilette, frischwasser, strom, grauwasser, abfall, dusche
- Ausflüge / schöne Orte: normale experience-POIs und mixed-POIs mit Erlebniswert
- Priorität bei Mehrfachzuordnung: Stellplatz vor Camper-Service vor Ausflug

### Bestätigte Tests

- `python3 scout4u_score.py --self-test` -> Self-Test OK
- Camper-Testlauf rainy mit Profil V zeigt Stellplatz Eichholz unter Stellplätze
- Öffentliche Toilette Bahnhof und Camper-Service Wankdorf erscheinen unter Camper-Services
- Profil-A-Testlauf rainy zeigt Beatushöhlen, Zentrum Paul Klee, Rosengarten Bern und Gurten Panorama unter Ausflüge / schöne Orte
- --show-filtered funktioniert weiterhin

### Offene Designfrage

- Die Überschrift "Empfehlungen" plus direkt folgende Gruppenüberschriften wirkt noch etwas technisch/doppelt und kann später für die Demo-Ausgabe geglättet werden.
