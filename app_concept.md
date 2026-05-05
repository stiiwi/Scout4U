# Scout4U App-Konzept

## Kurzbeschreibung

Scout4U ist ein smarter Reisebegleiter fuer Camper und Camping-Reisende. Die App soll unterwegs passende Orte vorschlagen: zum Uebernachten, fuer Versorgung und Services sowie fuer Ausfluege vom aktuellen Reise- oder Campingort aus.

Scout4U ist bewusst mehr als eine reine Stellplatz-App. Der Wert entsteht daraus, dass Empfehlungen spaeter Standort, Radius, Wetter, Reisebeduerfnis, Ortstyp, verfuegbare Services und Datenverlaesslichkeit zusammen denken.

## Zielgruppe V1

V1 richtet sich an Camper- und Camping-Reisende, die unterwegs schnell gute Entscheidungen treffen wollen:

- Wo kann ich heute sinnvoll stehen?
- Wo bekomme ich Wasser, Strom, WC-Entsorgung, Dusche oder Toilette?
- Was lohnt sich in der Naehe, wenn das Wetter gut oder schlecht ist?
- Welche Orte wirken verlaesslich genug, um sie anzufahren?

Die erste Zielgruppe ist praktisch orientiert, nicht technisch. Scout4U soll ruhig, klar und hilfreich wirken, ohne die Nutzerin mit Rohdaten oder internen Scores zu belasten.

## Hauptnutzerfluesse

### Ich suche einen Stellplatz

Die Nutzerin oeffnet Scout4U in der Naehe ihres aktuellen Reiseortes und waehlt Uebernachten / Stellplaetze. Scout4U zeigt passende Stellplaetze im Radius, mit Entfernung, Richtung, Preisangabe, wichtigen Services und einem kurzen Entscheidungsgrund.

Spaeter sollte dieser Fluss echte Standortdaten, Radiuslogik, Verfuegbarkeit, Quellenstand und Route/Website beruecksichtigen.

### Ich brauche Versorgung

Die Nutzerin wechselt zu Services, weil sie Frischwasser, Entsorgung, Strom, Dusche oder Toilette braucht. Scout4U priorisiert Orte, die den konkreten Bedarf erfuellen, und unterscheidet Versorgung von Stellplaetzen und Ausflugsorten.

Spaeter sollte dieser Fluss konkrete Servicearten, Oeffnungszeiten, Kosten, Zugangsbedingungen und Datenverlaesslichkeit deutlich machen.

### Ich suche einen Ausflug abhaengig vom Wetter

Die Nutzerin waehlt Erleben und sieht Ausfluege vom Reise- oder Campingort aus. Bei Sonne werden offene Natur-, Aussicht- und Wasserorte attraktiver. Bei Regen werden Indoor-, Kultur- oder wettergeschuetzte Orte staerker.

Services sollen dabei wetter-neutral bleiben. Der Wettereffekt gehoert vor allem in den Erlebnisbereich und soll erklaeren, warum ein Ort heute gut passt.

### Ich pruefe Details und starte spaeter Route/Website

Die Nutzerin oeffnet die Details einer Karte, prueft Services, Hinweise, Quelle und letzten Pruefstand. Wenn echte Daten vorhanden sind, startet sie spaeter Route oder Website aus Scout4U heraus.

Aktuell sind diese Aktionen in der Demo nur vorbereitet. Fuer eine echte App braucht jeder Ort saubere Detaildaten, Koordinaten oder ableitbare Kartenlinks, Website-URLs und Angaben zur Verlaesslichkeit.

## Was aktuell nur Demo ist

- `demo.html` ist eine statische HTML-Demo, erzeugt aus `generate_demo_html.py`.
- Die Demo nutzt Beispiel-CSV-Daten rund um Bern.
- Wetter ist ein statischer Regen/Sonne-Schalter.
- Radius und Standort sind noch keine echte App-Logik.
- `distance_km` und `direction` kommen aus den Beispieldaten, nicht aus GPS oder Routing.
- `lat` und `lon` sind in den Camper-Beispieldaten aktuell leer.
- Website- und Routendaten sind vorbereitet, aber noch nicht mit echten Quellen gefuellt.
- Merkliste und Details sind lokale Demo-Interaktionen.
- Es gibt keine API, keine Datenbank, keine echte Karte und keine mobile App.

## Was spaeter echte App-Logik werden soll

- Standort und Radius als echte Eingabe oder automatische Erkennung.
- Entfernung und Richtung aus Koordinaten berechnen.
- Wetterdaten fuer den aktuellen Ort und Zeitraum einbeziehen.
- Modi wie Uebernachten, Versorgung, Erleben oder kurz & praktisch als klare Produktsicht.
- POI-Typen und Kategorien sauber trennen.
- Services als strukturierte Daten bewerten.
- Details mit Website, Kartenlink, Quelle, Pruefstand und Verlaesslichkeit anzeigen.
- Empfehlungen nachvollziehbar begruenden, ohne interne Score-Details offenzulegen.
- Datenqualitaet und Aktualitaet in die Empfehlung einfliessen lassen.

## Bewusste Nicht-Ziele fuer jetzt

- Keine neue App-Struktur bauen.
- Keine API bauen.
- Keine Datenbank einfuehren.
- Keine echte GPS- oder Kartenintegration.
- Keine Android- oder iOS-App beginnen.
- Keine Migration der CSV-Daten in JSON oder ein anderes Speicherformat.
- Keine weitere Feinarbeit an kleinen visuellen Details der bestehenden Demo.
- Keine Monetarisierung, Login- oder Nutzerkonto-Funktionen.
