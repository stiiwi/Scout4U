# Scout4U Datenmodell-Skizze

Diese Skizze beschreibt ein spaeteres Ort-/POI-Datenmodell fuer Scout4U. Sie ist noch kein technischer Migrationsplan und keine Datenbank- oder JSON-Struktur. Die bestehende CSV-Demo bleibt vorerst die Arbeitsbasis.

## Grundidee

Ein Ort soll genug strukturierte Informationen enthalten, damit Scout4U ihn spaeter fuer drei Produktbereiche bewerten kann:

- Uebernachten / Stellplaetze
- Services / Versorgung
- Erleben / Ausfluege

Gleichzeitig soll sichtbar bleiben, wie verlaesslich ein Ort ist und ob wichtige Detaildaten wie Website, Koordinaten oder Pruefstand vorhanden sind.

## Vorgeschlagene Felder

| Feld | Wofuer ist es da? | Pflicht? | Status |
| --- | --- | --- | --- |
| `id` | Eindeutiger stabiler Schluessel fuer einen Ort. Wichtig fuer Merkliste, Updates, Deduplizierung und spaetere Verknuepfungen. | Pflicht | Heute genutzt. |
| `name` | Anzeigename des Ortes auf Karten, Listen und Detailseiten. | Pflicht | Heute genutzt. |
| `poi_type` | Grober Ortstyp, z. B. `experience`, `camper_service` oder `mixed`. Trennt Ausfluege, Services und Mischorte. | Pflicht | Heute genutzt. |
| `category` | Nutzernahe Produktkategorie, z. B. `stay`, `supply`, `toilet`, `excursion`, `museum`, `viewpoint`. Hilft spaeter bei Filtern und App-Navigation. | Optional | Spaeter. Aktuell wird Kategorie aus Typ, Services und Tags abgeleitet. |
| `lat` | Breitengrad fuer Karten, Entfernung, Richtung und Routenstart. | Optional bis echte Orte gepflegt sind, spaeter fuer App Pflicht. | Heute vorbereitet, in Camper-Daten aktuell leer. |
| `lon` | Laengengrad fuer Karten, Entfernung, Richtung und Routenstart. | Optional bis echte Orte gepflegt sind, spaeter fuer App Pflicht. | Heute vorbereitet, in Camper-Daten aktuell leer. |
| `direction` | Grobe Richtung vom Reiseort, z. B. Sued, Nordost oder Zentrum. Nuetzlich, solange keine echte Karte vorhanden ist. | Optional | Heute genutzt in der Demo. |
| `distance_km` | Entfernung vom aktuellen oder angenommenen Standort. In der Demo statisch, spaeter berechnet. | Pflicht fuer Demo, spaeter berechenbar aus Koordinaten. | Heute genutzt. |
| `price_label` | Nutzernahe Preisangabe, z. B. kostenlos, CHF 18 / Nacht oder CHF 4 / Dusche. Entkoppelt Anzeige von reiner Zahl. | Optional | Spaeter. Heute gibt es `price_chf` und abgeleitete Labels. |
| `opening_hours` | Strukturierte oder textliche Oeffnungszeiten und Zugangsregeln. Wichtig fuer Services, Museen und wetterabhaengige Ausfluege. | Optional, aber empfohlen fuer oeffnungszeitenrelevante Orte. | Spaeter. Heute gibt es nur `oeffnungszeiten_relevant` und `vermutlich_offen`. |
| `services` | Strukturierte Liste verfuegbarer Camper-Services, z. B. Frischwasser, WC-Entsorgung, Dusche, Strom, Abfall, Toilette. | Optional, Pflicht fuer Service- und Stellplatz-POIs. | Heute genutzt. |
| `weather_suitability` | Beschreibung oder strukturierte Werte, wann ein Ort wetterlich gut passt, z. B. `rainy_good`, `sunny_good`, `indoor`, `covered`, `exposed`. | Optional | Spaeter. Heute wird Wetter grob aus `indoor_anteil` und Tags abgeleitet. |
| `tags` | Interessen-, Erlebnis- und Eigenschafts-Tags, z. B. Natur, Aussicht, Kultur, familienfreundlich, fotogen. | Optional, aber wichtig fuer Empfehlungen. | Heute genutzt. |
| `source` | Herkunft der Daten, z. B. Demo, manuelle Recherche, offizielle Website oder andere Quelle. Wichtig fuer Vertrauen. | Optional, spaeter empfohlen. | Teilweise heute genutzt als `datenquelle`; Detailfeld `source` ist vorbereitet. |
| `last_checked` | Datum oder Stand der letzten Pruefung. Wichtig fuer Oeffnungszeiten, Preise, Services und Verlaesslichkeit. | Optional, spaeter empfohlen. | Heute vorbereitet, aktuell meist leer. |
| `website_url` | Link zur offiziellen Website oder einer verlaesslichen Detailseite. | Optional | Heute vorbereitet, aktuell meist leer. |
| `maps_url` | Direkter Karten- oder Routenlink, falls manuell gepflegt. Alternativ aus `lat` und `lon` ableitbar. | Optional | Spaeter. Heute wird ein Google-Maps-Routenlink nur aus Koordinaten abgeleitet, wenn vorhanden. |
| `notes` / `description` | Kurzer menschenlesbarer Hinweis: Besonderheiten, Einschränkungen, Zugang, Demo-Kontext oder Beschreibung. | Optional | Heute genutzt als `notes`. |
| `reliability` | Einschaetzung der Datenverlaesslichkeit, z. B. `low`, `medium`, `high` oder ein spaeteres Punktesystem. Kann Quelle, Pruefstand und Vollstaendigkeit zusammenfassen. | Optional, spaeter wichtig. | Spaeter. |

## Match-Gruende / Profiltreffer

Scout4U sollte spaeter nicht nur einen Gesamtscore berechnen, sondern nachvollziehbare Match-Gruende ableiten. Diese Gruende sind die Bruecke zwischen Rohdaten, Profil, Kontext und Kartenanzeige. Sie sollten strukturiert genug sein, um sortiert, gewichtet und sichtbar oder intern genutzt zu werden.

### Arten von Gruenden

| Art | Beispiele | Quelle im Modell | Sichtbarkeit |
| --- | --- | --- | --- |
| Profiltreffer | fotogen, familienfreundlich, ruhig, guenstig, hundefreundlich | `tags`, Profilinteressen, spaetere Nutzerpraeferenzen | Gute sichtbare Kandidaten als kurze Chips, wenn sie fuer die Entscheidung hilfreich sind. |
| Service-Merkmale | Wasser, Strom, WC-Entsorgung, Dusche, Toilette, Oeffnungszeiten, Kosten | `services`, `opening_hours`, `price_label`, spaetere Detaildaten | Bei Stellplaetzen und Versorgung sehr wichtig; sichtbar als Service-Chips oder Fakten, nicht als langer Satz. |
| Kontextsignale | nah, im Radius, wettergeschuetzt, draussen, lohnender Umweg, Route moeglich | Standort, Radius, Wetter, `distance_km`, `weather_suitability`, `lat`/`lon` | Sichtbar, wenn sie die aktuelle Situation erklaeren; z. B. nah, wettergeschuetzt oder lohnender Umweg. |
| Ausschluss- und Warnsignale | ausserhalb Radius, unklare Daten, fehlende Serviceangaben, Oeffnungszeiten pruefen | Filterlogik, `reliability`, fehlende Felder, Pruefstand | Eher intern fuer Filter/Ranking oder in Details/Warnhinweisen; nur sichtbar, wenn es die Entscheidung direkt beeinflusst. |

### Sichtbar vs. intern

Sichtbar auf Karten sollten vor allem positive, kurze und entscheidungsnahe Gruende erscheinen: wichtige Services, Profiltreffer und aktuelle Kontextsignale. Beispiele sind `Wasser`, `Strom`, `fotogen`, `familienfreundlich`, `nah`, `wettergeschuetzt` oder `lohnender Umweg`.

Intern bleiben sollten technische Score-Bestandteile, harte Filtergruende und Rohdatenqualitaet, solange sie nicht unmittelbar handlungsrelevant sind. Datenqualitaet, Quelle und Pruefstand koennen spaeter in Details, Warnungen oder einem Vertrauensmodell auftauchen, sollten aber nicht jede Hauptkarte dominieren.

Die aktuelle Demo-Zeile `Heute sinnvoll: ...` ist eine Uebergangsloesung, um diese Logik sichtbar zu testen. Langfristig sollten die gleichen Informationen eher als gut priorisierte Chips, Fakten oder Statussignale auf Karten erscheinen.

## Hinweise fuer die aktuelle Phase

- Das Modell soll zuerst Produktklarheit schaffen, nicht sofort Technik erzwingen.
- Die bestehende CSV kann vorerst weiter als Demo-Datenquelle dienen.
- `distance_km` und `direction` sind im Prototyp praktisch, auch wenn sie spaeter aus echten Koordinaten berechnet werden koennen.
- `maps_url` muss nicht zwingend gespeichert werden, wenn ein sauberer Link aus `lat` und `lon` ableitbar ist.
- `reliability`, `source` und `last_checked` sollten spaeter zusammen betrachtet werden, weil sie direkt beeinflussen, wie vertrauenswuerdig eine Empfehlung wirkt.
