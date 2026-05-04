# Nutzertest Scout4U – Eltern (2026-05-04)

## Kontext

- Erster Test der HTML-Demo mit den Eltern (Mutter als primäre Testerin, Vater als zweiter Beobachter).
- Demo: statische Ein-Seiten-HTML-Demo, drei Hauptkategorien (Übernachten, Services, Erleben).
- Vorgehen: freies Ausprobieren am Laptop, Gespräch begleitet.
- Quelle: Audio-Transkript des Tests (siehe Anhang) plus eigene Notizen während/nach dem Test.

## Beobachtetes Verhalten

- Mutter findet sich ohne Erklärung intuitiv in der Demo zurecht.
- Stolperstelle 1: Demo wirkt am Laptop „wie ein schmaler Streifen in der Mitte". Wunsch nach mehr Breite, Vorschlag 2 Spalten.
- Stolperstelle 2: Mutter klickt **oben** auf die Kategorie-Kacheln (Übernachten/Services/Erleben), erwartet sie als Tabs. Zum Testzeitpunkt reagierten sie noch nicht. Sie hat das Verhalten unaufgefordert mehrfach versucht.
- Stolperstelle 3: Die Trennung „Erleben" vs. „Natur/Ausflüge ansehen" wurde als zwei getrennte Modi wahrgenommen. Verwirrung, obwohl es nur ein Demo-Artefakt war.
- Den „Warum passt das?"-Button hat sie nicht entdeckt.

## Meta-Hinweis vom Vater

> „Vielleicht müssten wir noch ein bisschen unterscheiden zwischen: Das wäre die geniale, perfekte App und das ist jetzt mal die erste Version. Du bist schon bei 2.5."

Ernst nehmen: schützt vor Scope Creep nach Feedback-Sessions.

## Wünsche und Vorschläge aus dem Gespräch

### Layout / Interaktion
- Demo am Laptop breiter, 2 Spalten für Karten.
- Obere Kategorie-Kacheln direkt klickbar als Tabs.
- Wenn obere Kacheln Tabs sind, sind die unteren Tabs ggf. redundant.
- „Natur/Ausflüge"-Modus aus Demo entfernen, in „Erleben" integrieren.

### Services / Inhalte
- Pro Service-Karte sichtbar: Frischwasser, WC-Entsorgung, Kosten, Öffnungszeiten.
- Hinweis: Öffnungszeiten in der Praxis schwierig, Daten oft unzuverlässig.
- WC-Entsorgung an Autobahnen (CH/DE) ist online schwer zu finden – Datenquelle bleibt offen.

### Standort und Profil
- Standort wählbar machen: GPS, Postleitzahl oder Koordinaten.
- Suchradius einstellbar (Camper anders als Velo, Wanderer, Auto).
- Reisemodus im Profil: Camper, zu Fuß, Velo, Auto, Wanderer.
- Bed & Breakfast / günstige Unterkunft als Fallback, wenn kein Stellplatz gefunden. Im Profil aktivierbar.

### Rechtliches / Wildcamping
- Pro Standort/Region rechtliche Lage zu Wildcamping anzeigen.
- Beispiele genannt: CH gemeindeabhängig, DE oft in Nationalparks verboten, Island/Kroatien striktes Verbot.

### Notizen vom Tester selbst (Ergänzung nach Aufnahme)
- Einzelne gespeicherte Orte löschen können.
- Gespeicherte Orte im Profil persistieren.
- Gespeicherte Orte als Dropdown, erste 3 sichtbar, Rest aufklappbar.
- Bei gemerkten Orten Kategorie sichtbar (Services/Übernachten/Erleben).
- Button „Route anzeigen" vom aktuellen Standort zum Ort.
- Bei Distanz zusätzlich Himmelsrichtung anzeigen (z. B. „22 km NO").
- Sprachumschaltung, ggf. im Profil gespeichert.
- Später: Nutzerbewertungen.
- Idee: Karten/Fenster mit Maus frei vergrößerbar – eher kritisch, siehe Bewertung.

### Vision / Geschäft (am Rand erwähnt)
- Login mit Google denkbar.
- Community-/Moderations-Thematik kurz angerissen, kein konkreter Wunsch.
- Name „Scout4U" – im Gespräch geprüft, scheint frei zu sein.

## Status nach Test

### Bereits umgesetzt (laut aktuellem Demo-Stand)
- Obere Kategorie-Kacheln sind klickbare Filter.
- „Warum passt das?"-Button entfernt.
- Erleben/Ausflüge zu einem Tab konsolidiert.
- Merkliste eingeklappt, nach Kategorien gruppiert.
- Orte in Merkliste anklickbar (Sprung zur Karte) und entfernbar.
- Service-Chips direkt auf Karten sichtbar.

### Offen – kategorisiert

**Muss (klein, hoher Mehrwert, ohne Backend machbar)**
- 2-Spalten-Layout ab Desktop-Breakpoint.
- Himmelsrichtung in Distanz-Anzeige (CSV-Wert + Anzeige-Snippet).
- Bei gemerkten Orten Kategorie pro Eintrag sichtbar (falls Gruppen-Heading nicht reicht).

**Sollte (sinnvoll, aber nicht V1.0-blockierend)**
- Merkliste: nur erste 3 anzeigen, Rest aufklappbar.
- Service-Karten um Frischwasser/WC/Kosten/Öffnungszeiten ergänzen (statisch).
- Profil als sichtbarer Mock im UI andeuten (Reisemodus-Auswahl).
- Sprachumschaltung als sichtbarer Platzhalter im Profil-Bereich.

**Später (V1.x oder V2)**
- Standortwahl (GPS, PLZ, Koordinaten).
- Radius einstellbar.
- Bed & Breakfast als Fallback.
- Wildcamping-Rechtslage pro Standort.
- Route vom aktuellen Standort.
- Login mit Google.
- Nutzerbewertungen / Community.
- WC-Entsorgungs-Datenquellen integrieren.

**Eher nicht / kritisch**
- Frei mit der Maus vergrößerbare Karten-Kacheln. Hoher Bauaufwand, fragile Interaktion, Mehrwert wird vermutlich schon durch 2-Spalten-Layout erreicht.

## Empfohlener nächster Schritt

Eine kleine Änderung als nächstes: Himmelsrichtung in der Distanz-Anzeige ergänzen (z. B. „22 km NO"). Sehr sichtbar, trivial in der statischen Demo umsetzbar, zahlt direkt auf den Camper-Use-Case ein. Direkt im selben Schritt das 2-Spalten-Desktop-Layout aktivieren.

---

## Anhang: Rohtranskript

> Hinweis: Audio-Transkript, schweizerdeutsch geprägt, mit typischen Transkriptionsfehlern und Wiederholungen. Hier bewusst unverändert abgelegt, damit die Auswertung oben nachvollziehbar bleibt.

```
Wie groß ist es? Oder nicht? Ja, das ist für Juna. Das ist für Juna. Aha. Ja, das sollte wohl kein Roller spielen.

Das ist für Juna. Aber der Juna ist für Juna. Das sollte doch kein Roller spielen. Eigentlich nicht, nein. Hast du das? Stimmt, Thomas? Ja, das ist richtig.

Oh, das ist schon gut. Ich habe eine Demo mit Beispiel. Ja. Auf dem laptop sind wir dann noch. Ja. Super. Und jetzt eigentlich ohne, dass ich groß viel muss sagen, Fingert ihr nachher irgendwie zurecht? Fingert ihr was? Also... Schönen Sie das? Ja, ich weiß. Schönen Sie das? Ja, ich weiß.

Ich bin immer noch. Wie ist die Größe auf dem Handy? Ja, gut. Es ist so einfach in der Mitte so einer Balken, aber das ist einfach... Also... Ja, sollte sie noch ein bisschen breiter sein eigentlich auf dem Laptop, he?

Ja, das habe ich mir auch schon gedacht. Das wollte ich dann auch noch machen, dass es ein bisschen breiter ist. Ja, jetzt ist es einfach ein schmaler Spicer. Ja. Wie gleich ausgehen, wie auf dem Handy, oder?

Okay. Ja, okay. Ja, okay. Ja, also... Ja. Hier ist es eben vorhin ein bisschen breiter gewesen, aber in diesem Fall ist es noch nicht final so, wie es so ist. Ja, zwei Spalten machen, weisst du, dass du mehr siehst auf dem Mord. So, man ist einfach immer ab und auf dem Handy auf dem Laptop, oder?

Ja, klar. Das ist eine gute Idee. Ja, zwei oder drei, oder? Also... Die meisten haben einen recht breiten Bildschirm, oder? Ja, gut. Ja, das stimmt. Gut. Ja, das stimmt. Wenn man dann auch noch ein Laptop, wenn man wirklich unterwegs ist, vielleicht nicht.

Das ist der, wo wir haben, oder? Also ja, gut. Die anderen haben trotzdem auch große Auflösungen, oder? Ja, ja. Ja, das ist gut. Das ist notiert. Die Services, wo haben wir denn dort?

Ja, die anderen Services, Dusche und Toilette. Übernachten haben wir, aber die Services nicht drauf gedrückt, wenn wir Strand rauswählen und dann... Und? Aber es hat eigentlich vieles auf dem Set. Was du das noch machen, dass man oben, wenn man auf Übernachten drückt, weisst du gerade...

Ja. Wenn die Felder dort, wo drei Übernachtungen, sechs Services und Reise erleben hast, dass man das gerade anklicken kann und dann auch wechselt automatisch auf Services oder halt übernachtigen, oder? Aber da kannst du ja anklicken. Ja. Aber du willst uns oben... Ja, aber rein intuitiv.

Ich will jetzt Services sehen. Ich sage Services, oder? Ja, auch intuitiv. Ja, die Intuitiv. Oben anklicken. Du sehen, was passiert. Du hast auch unten angeklickt, Befa.

Also, wo sollte man draufklicken können? Ich habe das nicht ganz verstanden, oder? Ja, genau. Du hast oben drei so... Nicht Buttons, sondern einfach so drei Räume.

Und am ersten steht drei Übernachten, oder? Und dann hast du sechs Services und ein Erleben. Ja, genau. Und wenn du jetzt dort drauf drückst, dann passiert nichts, oder? Ja, dass man oben gerade drauf drücken kann.

Okay. Ja, ja, ja. Ja. Wenn man das intuitiv gerade drauf drückt, dann ist nichts passiert, oder? Mhm. Und wenn man das noch kombinieren könnte... Genau. Eigentlich bricht uns die unteren Tabs gar nicht. Eigentlich so, ob man oben wechseln zwischen den verschiedenen Reitern.

Genau. Das ist eine gute Idee, ja. Ja. Ja. Gut. Das, was dann einfach Zeit, wie viel es hat. Ja, ja. Genau. Das kann man nicht mehr als Buttons. Ja, ja. Genau. Hat ihr schon gesehen, man kann auch noch auf einen anderen Modus wechseln.

Auf eine Naturaussicht, Ausflügeansehen. Könnt ihr drücken dort. Ja, ja. Ja, ja. Und das ist dann nochmal wie ein anderer Einführer. Ah. Das wäre doch auch einer, der oben rein schenken kann, oder?

Das ist nur zur Demo. Das ist nur für die Demo, weisst du? Ja, ja. Aber ich meine, weisst du, oben hast ja jetzt Übernachtenservices und Erleben, oder? Genau. Da könntest du dann gleich einen machen, der Ausflüge drinnen hat.

Genau. Das wäre dann gedacht im Erleben, eigentlich. Das sind dort dann so Sachen, die man einfach machen kann und so, ja. Mhm. Wo kann man ausfällen, an die Natur oder was? Ich habe noch nicht gesehen.

Äh, wo ich noch... Wir können auch nicht Profile machen und so, wo du selber auswählen kannst. Nein. Aber du kannst unten, also ab jedem Feld, auf warum passt das drücken. Und dann zeigt es dir an, wieso es dir das anzeigt quasi.

Und was es dort hat. Ja, das ist die Möbel, die du da oben hast. Ja. Das habe ich jetzt nicht gesehen. Das ist irgendwie umgegangen.

Natur und Aussicht, Ausflügeansehen. Aber eben, dass gerade oben in die drei Felder reinnehmen, die du da oben hast. Ja. Und ich denke, das ist separat, oder? Aber oben, wenn es gerade so in den Gefierfeldern kann...

Braucht das Gefier von dir ausgesehen? Braucht das Erleben und Ausflügen getrennt? Ist das nicht in den Überzeugungen? Mhm. Oder was würdest du jetzt erleben in einer anderen, was in den Ausflügen?

Ja, genau so, wie du es jetzt getrennt hast. Also, oder? Ausflüge, also... Soll ich das sagen. Wenn du jetzt reingehst und die drei hast, dann hast du ja das Natur- und Aussicht-Ausflügeansehen. hast du ja auch noch zur Auswahl unten, oder? Das hast du ja immer zur Auswahl.

Egal, ob du in den Services reingehst oder in Erleben. Also, warum ich gerade die Dinge reinnehme. In die obere Auswahl. Ich komme wieder zurück.

Ich komme nicht raus, was du meinst. Sorry. Weisst du, bei Erleben hast du das Schloss Burgdorf. Genau. Und dann gibt es den Rosengarten und den Rosengarten und die Gurtpanoramas und Sockorn. Genau. Die werden dann implementiert in das andere.

Das habe ich auch gesagt. Aber was ist jetzt der Unterschied zwischen dem Schloss Burgdorf und den Rosengarten, die es dann noch hat? Das ist eigentlich kein Umschlag. Eben, das ist doch einfach der dritte.

Also, es braucht doch nur drei, oder? Ja, das ist das andere Ding nicht. Genau. Das habe ich ja vorher schon gesagt. Das sind nicht zwei Seiten, die es gibt.

Das wird dann in das andere implementiert. Das ist einfach nur noch mal für die Demo. Das ist eben noch der zweite. Ja. Das rede ich auch extra für die Demo.

Das kommt dann auch nicht in die Finale ab. Was steht das für Demo? Also, es ist einfach so ein solcher Tagetag, wo du auch als Flüger vom Reisecamping-Wort aus... Ja. Wie gesagt, die zweite Seite ist nicht...

Das ist alles jetzt einfach mal, euch die zwei Sachen zu zeigen. Das wird dann definitiv nicht separat sein. Das wird dann alles... Das wird dann alles in diesem dritten Tab drin sein.

Ob ich erleben oder alles flüge. Okay. Aber meine Frage ist darum vorher gewesen: Braucht es denn erleben und alles flüge getrennt, dass man vier Tabs macht, oder... Nein, nein, nein, nein. Würde man sie in der drei zusammenfassen?

Wenn man die Tabs integriert, dann ja nicht. Nein, dann braucht es nicht vier. Genau. Das war meine Frage. Super. Dann ist gut. Dann mache ich das so.

Ich bin mit nach Papa. Ähm... Was ist sonst noch? So wie bei den Services. Ist das das, was ihr etwa braucht?

Oder würdet ihr noch mehr Sachen? Ich habe nur noch WC, Frischwasser, Daten, oder... Weisst du, das sind momentan alles nur Textdaten, gell? Ihr App wird dann dann aus dem Internet generiert durch die Standorte.

Momentan ist das alles in der Tabelle. Okay. Nein, das sind so die Sachen für die Camper-Services, wo man Frischwasser holen oder WC entsorgen kann. Ja. Das sind solche Toiletten, die man braucht. Ja. Ja, und das ist wichtig, oder?

Frischwasser, WC entsorgen und wie viel das kostet. Das ist die Top. Ja. Und die Öffnungszeiten, oder? Ja, wenn es hat.

Ja, voll. Ja, das habe ich auch schon besprochen, dass wir das einfach einfügen, aber dass es manchmal auch kompliziert ist mit der Öffnungszeiten, aber das finde ich schon ein Wert. Ja, ja, ja. Und die Öffnungszeiten sind ja auch nicht gewähren, oder? Das ist ja klar. Das ist so klar.

Das ist klar, ja. Ja, das ist immer etwas anderes. Aber es ist, weisst du, direkt hat dann das Wetter geschützt, so die Sachen, das ist auch immer gut, wenn man sich dann gesehen. Und die Ferne, und man hat dann noch die Kante genachten dort.

Das ist einfach schon schon alles gut, gell? Ja. Sehr gut. Auch für eine WC, das ist mal eine frühe erste Version. Das wird jetzt schon noch weiter... Ja, natürlich. Aber in diesem Fall die Buttons oben direkt direkt zum Klicken machen, dass es nicht zweimal ist.

Das macht mega Sinn, dass wir die so umsetzen. Ja. Dann kannst du auch die Unterne rausnehmen, oder? Genau, ja. Oder wie du erst vorgesehen mit den gemerkten Orten. Du hast dort einfach ein paar Anzeigen und dann auch mit einer separaten Liste, die du dann auch raus erweitern kannst.

Weisst du, wenn du dann 30 Orte hast oder so. Ja. Dann kannst du nur die ersten fünf Anzeigen, die ersten drei und dann auch anfangen zum Weiterblättern im Feld selber oder ein neues Landstern anzeigen, das kannst du auswählen. Mhm. Oder dass es dir auch nur die gemerkten Orte anzeigt, von denen du gerade bist.

Oder wenn du in einer Bretagne seid, dann sollte es eigentlich auch nur die gemerkten Orte anzeigen, die ihr vielleicht im letzten Ausflug in dieser Region gemerkt habt. Ja, ja. Und nicht die von Italien, die wollen dann auch nicht sehen. Die wollen dann auch nur die von den, die gerade in der Region sind.

Das ist richtig, ja. Ja. Wo kann man den Ort überhaupt auswählen? Momentan noch nicht. Das könnte man auch noch können. Ja, ja, klar. Man kann dann auch auswählen, entweder lokale Standorte verwenden, per GPS schauen, wo du gerade bist.

Oder man kann sagen, ich möchte von dieser und dieser Postleitzahl oder von dieser und dieser Koordinator oder was auch immer, kann man dann angeben, von wo man suchen möchte. Die Distanz zum nächsten kannst du auch eingrenzen. Ja, du hast es jetzt 25 Kilometer, oder? Ah, wie gross Radius soll sein?

Ja. Ja, das sollte man auch anpassen können, wie gross Radius soll sein. Ja. Weil wenn man mit Camper unterwegs ist, hat man einen anderen Radius, als wenn man am Zeltlen ist und mit dem Velter unterwegs ist, oder? Ja. Oder ein Wanderer. Oder ein Wanderer, ja. Ja. Wanderer, wie geht das schon aus unserem Leben nachher?

Ja, ja. Ich habe mir zuerst lange überlegt. Also zuerst dachte ich, ich wollte es ganz offen machen, die App für allgemeine Aktivitäten. Und dann dachte ich, das wäre für eine erste Version schon cool, wenn es auf Camper-Camping zugeschnitten wäre, weil ihr ja quasi meine ersten Kunden seid.

Ja. Aber ich habe es jetzt einfach so, einfach vom Aufbau der App her so gemacht, dass es wie erweitert werden kann und ja. Ja, dass man einfach seine Bedürfnisse quasi eintragen kann. Was anfängt, bist du im Camper unterwegs oder etwa zu Fuß? Ja, voll. Ja, voll. Mit dem Auto, weiss.

Kennst du den noch nicht? Ah ja. Irgendwelche Unkünfte, also Baden-Breakfests oder so, oder? Stimmt, das ist dann vielleicht aber für später, ja voll. Aber stimmt, man könnte ins Profil, könnte man dann wirklich rein tun, quasi, dass man wirklich angeben kann.

Man ist jetzt mit dem Camper unterwegs und so. Dass es dann dementsprechend Vorschläge gemacht hat. Ja. Aber eben, manchmal ist der Camper da froh, wenn er irgendwann einmal ein Spät-and-Breakfast hat, oder? Ja. Weisst du, es gibt auch diejenigen, die wir gerne duschen gehen und dann auch wieder mal in einem richtigen Bett liegen, auch wenn es unbequem ist.

Das stimmt, ja. Ja, voll. Nein, genau. Also, da geht es. Also, könnte das noch ein viertes Ding sein? Unterkunft? Hey, Lutz, ich würde es vielleicht so machen, dass man es im Profil einstellen kann, dass man gerne Unterkünfte hat. Weisst du, so, eben, in der Art. Ja, ja.

Eine zusätzliche Auswahl im Profil. Ja, ja. Und man quasi auf, ja. Und je nachdem braucht es einen Benito, oder? Den kannst du gerade ausblenden, oder?

Am besten machst du so Dinge, dann so... Wo es Grau wird, nachher. Ja, Grau oder das Höckli dran, wenn es ausgewählt ist. Ja, ja. Ich finde, wenn du im Camper unterwegs bist, das gehört so zu England.

Dann haben wir dann einen Asian Tramers bei den Breakfast genommen. Ja. Das wollen wir weggeben. Ja. Manchmal ist es auch gut, wenn du nicht unterwegs bist und einfach nichts findest, oder? Ja. Dass du dann noch gerne irgendeine Unterkunft hast.

Ja, klar. Okay, schantiert. Bed & Breakfast Optionen oder günstige Übernachtungsmöglichkeiten. Sehr gut. Wenn du nichts findest, in dem Umkreis, in dem du ausgewählt hast, oder? Ja. Dass du dann automatisch nach Bed & Breakfast oder billiger Unterkunft gesuchen. Weisst du, wie ich meine?

Wenn es keinen Stellplatz findet. Hä? Wenn es keinen Stellplatz findet, dass es nach Bed & Breakfast sucht. Ja. Okay. Ja, das haben wir auch schon gehabt. Weisst du, haben gesucht, weisst du nicht wie lange und tief nicht gefunden, oder?

Ja, ja. Und dann haben wir beschlossen, irgendwann ein Bed & Breakfast einzusetzen und dann zu holen. Aber dann würde ich automatisch, dass man dann halt auch nicht. Ja, vielleicht müssten wir noch ein bisschen unterscheiden zwischen: Das wäre die geniale, perfekte App und das ist jetzt mal die erste Version und jetzt schaffen wir mal auf Version 1.1 her, oder?

Weisst du, du bist schon bei 2.5, oder? Aber weisst du, einfach Ideen sammeln, oder? Mega gerne, mega gerne. Das musst du umsetzen.

Ja, ja. Auch wenn ich in Zukunft noch Ideen habe, können wir sehr gerne notieren und mir schicken und ich probiere das irgendwie einzubauen. Ja. Du musst jetzt schauen, ob du wirklich Stoffe behalten kannst, damit du die Hausnummer noch einbauen kannst. Ja, klar. Das mache ich auch schon. Zum Teil ist es noch dämlich mit den WC-Entsorgungen, oder?

Weil prinzipiell findest du die sehr schlecht in der Schweiz. Ja. Im Ausland ist es noch fast einfacher, oder? Aber in der Schweiz gibt es auch Dinge, die an der Autobahn Entsorgung stellen, oder? Ja. Aber du hast nirgendwo im Netz etwas vermerkt.

Und auf der Autobahn selber eben auch nicht, oder? Die zeigen es einem nicht einmal an mit irgendeinem Zeichen. Okay, krass. Die sind nicht bei mir rein, oder? Ja, da ist es gut, wenn es dir immer anzeigt.

Ich weiß es nicht. Vielleicht gibt es noch in einer Seite, wo du aufrufen kannst. Ja. Es gibt ja solche Camper-Seiten, wo sie ziemlich viele Informationen drin haben. Die müssen wir dann auch einbeziehen, oder?

Ja, ja. Einfach, wo man das Camper-WC lernen kann, ist schon wichtig. Ja, genau. Das ist sehr wichtig. Sehr gut, sehr gut. Vor allem die Tiere, die viel frei in der Welt campieren, oder?

Ja, genau. Und was du machen kannst, ist, wenn du das rausfindest, oder? Und dass du gerade schreibst, dass eigentlich das Wildcamp verboten ist. In diesem jeweiligen Ort, oder? Ah, ja, ja. Immer noch die rechtliche Lage dazu nehmen, am jeweiligen Standort, ob Wildcamp erlaubt ist. Ja, genau. Sehr gut.

Weil zum Beispiel in der Schweiz ist es sogar gemeinsam abhängig, oder? Ja. Weil grundsätzlich, wenn du das Gefühl hast, du bist nicht fahrfähig, oder? Dann kannst du die Karren auf die Seite stellen und eine Pause machen. Ja. Das können sie nicht verbieten.

Aber es gibt natürlich Gemeinden, die sagen, auf ihrem Gemeindengebiet kommt das gar nicht aufgrund, oder? Mhm. Wenn man schon bei der Gemeinde abfahren und irgendwann einmal anders gehen würde. Ja, klar. Aber übernachten und führe sich, so auf diese Art, können sie nicht verbieten. Ja. Wenn du einfach einen Campingstil rausnimmst und ein Führer machst, dann kannst du sie jetzt nicht mehr.

Ja, das ist nicht mehr so. Aber das ist ja nicht direkt relevant für das. Aber ja, das würde ich auch schauen. Ja. Ja, aber wenn du direkt an die Information herkommst, dann wäre es nicht schlecht.

Ja, sehr gut. Ja, Deutschland ist vielfach in der Nationaltag verboten. Ja. Ja. Ja, das würde das vielleicht immer wieder sein. Ja. Aber Island, Island ist allgemein ein Verboten, oder? Ja. Ja, das ist ja auch in den Ländern, wie heisst es, in Kroatien.

Ja, Kroatien. Ja, die haben ja ein absolutes Wildcampenverbot. Okay, ja. Das darfst du wirklich nicht, oder? Ja, ja. Ja, das ist ja auch noch ein paar Punkte. Ja, das ist ja auch.

Ja, das ist ja auch. Ja, ja. Du, ich würde mal alles sammeln und dann gebe ich mal alles in Kain und schauen wir mal, wie wir das umsetzen können, was sinnvoll ist, was machbar ist. Ja. Ich bin mega froh über euer Feedback. Also, ein Scout4U gibt es noch nicht, oder?

Das ist schon mal Glück. Das habe ich noch gar nicht gesucht, nein. Ja, suchen wir mal. Ah ja, du weisst du es.

Ja, ja. Also auf GitHub gibt es auch mal kein Projekt, das Scout4U heisst. Ja, das ist nämlich so doof und das hat es noch nicht gegeben. Ja, aber das heisst nicht, dass es die Engineering gibt. Ja, ja. Ja, klar. Und ja, so wäre es natürlich super, oder? Mhm.

Ja, ja, später mal noch so einen Link, wenn du nochmal Gelddienste mit, oder? Dass du einfach Geld von you eingeben kannst und dann auch ein Prinzess. Genau. Ja, nicht schlecht. Ja, das ist schön. Ja. Das ist schön. Ja. Ich weiss nicht, das ist schön.

Das ist eine andere Frage, oder? Ob es dir wirklich mega viel hilft oder ob es, ja. Aber immerhin, der Vorteil ist, wir kennen den Entwickler und können immer eigene Wünsche anbringen. Ja, natürlich ist es super.

Wir haben schon Vorteile. Ja, genau. Es ist doch immer wichtig, weisst du, wenn die Entwickler mit der Community zusammenarbeiten. Ja, genau. Ja, gut. Wenn du irgendein Ding machst, wo sich einen Feintech gibt, der wirst du schon in ein Problem bekommen. Ja. So machen, dass sie nicht irgendwelche Müllfälle reinstellen.

Das ist klar, ja. Mhm. Ja, der strikt die Überwachungs-Policy, die ich die Meinungsfreiheit nicht ausleben lassen lassen lassen. Ja, genau. Ja, genau. Ich habe so Eintreif wie der Trumps in einem Anschluch, dass du das einfach da reinlässt. Genau. Ja, das ist eine coole Sache. Ja, cool. Ja, danke.

Ja, das war's. Ja, das war's. Ja, das war's. Ja, das war's. Ja, das ist eine coole Sache. Ja, cool. Danke, Freude. Ja, das war's. Ja, das war's. Ja, das war's. Ja, das habe ich schon so ein bisschen als Hinweis hergegeben, ja. Ja, ja, ja. Ja, ja, ja. Aber eben, das coole, weisst du, rein zu UI, das ist dann noch nicht, das heisst, das hat es mir gehabt, ich auch gesagt, das soll jetzt mal irgendetwas nehmen und das mal lassen.

Das ist wirklich etwas, das man dann auch einbekommen, fertig machen kann, wenn ein bisschen mehr vor der App steht. Ja. Und es macht auch noch nicht Sinn, jetzt immer wieder am UI rumzubasteln. Nein, das ist alles auch. Ja, das ist eine Funktion.

Vielleicht ist das Bild, und dann kannst du immer noch am anderen rumzubasteln. Genau, genau. Das Campingreisebegleiter, das würde dich vielleicht noch etwas ändern. Das kann ja auch so ein bisschen gut sein, das mit, weisst du auch nicht, mit dem Flutzeilunterbetchen, oder? Oder mit dem Velour. Ja. Ja. Ja.

Aber jetzt am Anfang ist es so etwas auf Camping halt spezialisiert. Das haben wir auch so gemacht, dass es jetzt mal für die erste Demo so war. Ja. Ja. Aber ja, ist gut. Cool. Also, der Beenditaufnahme. Und das Wetter, ist das Wetter nicht mehr drauf?

Vom Wetter haben wir noch so noch das Wetter. Ich glaube es, es zeigt doch immer anhand des Wetter. Es hat eine Logik dabei, die Punkte verteilt. Je nach Location checkt es mit Wetter und alles.

Und dann rechnet es so eine Skala, was es einem wie anzeigt und so. Ja. Umso mehr Punkte eine Location hat, anhand der Eingänge, Parameter und vom Wetter, wird es dann höher priorisiert. Okay. Gut, aber jetzt beendet die Aufnahme.

[Eigene Notizen nach Aufnahme]
Option, einzelne gespeicherte Orte löschen. Diese sollten dann auch im Profil gespeichert werden. Gespeicherte Orte in einem Drop-Down anzeigen, sonst kann es zu lang werden. Vielleicht die ersten 3 anzeigen. Bei gemerkten Orten: bei diesen sollte ersichtlich sein, zu was sie gehören (Services, Übernachten, Erleben). Idee: Button zum Anklicken, der einem die Route zeigt vom aktuellen Standort zum jeweiligen Ort. Und dazu bei der Anzeige, wie weit die Location entfernt ist, eine Angabe machen bezüglich der Himmelsrichtung. Also ob es 20 km Richtung Norden oder Richtung Süden ist. Das kann eine grosse Rolle spielen im Ernstfall. (N, S, SO, SW, NO…) Möglichkeit die Sprache zu ändern. (Vielleicht auch im Profil gespeichert.) Für später: Bewertungen von Nutzern. So sehen andere später, welche Orte beliebt sind und welche nicht. Idee: Die Felder (also die Fenster im Browser) sollten mit der Maus vergrösserbar sein, damit man sich die „Kacheln" so hinschieben kann wie gewünscht.
```
