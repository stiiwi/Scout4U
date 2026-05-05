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

## Hinweise fuer die aktuelle Phase

- Das Modell soll zuerst Produktklarheit schaffen, nicht sofort Technik erzwingen.
- Die bestehende CSV kann vorerst weiter als Demo-Datenquelle dienen.
- `distance_km` und `direction` sind im Prototyp praktisch, auch wenn sie spaeter aus echten Koordinaten berechnet werden koennen.
- `maps_url` muss nicht zwingend gespeichert werden, wenn ein sauberer Link aus `lat` und `lon` ableitbar ist.
- `reliability`, `source` und `last_checked` sollten spaeter zusammen betrachtet werden, weil sie direkt beeinflussen, wie vertrauenswuerdig eine Empfehlung wirkt.
