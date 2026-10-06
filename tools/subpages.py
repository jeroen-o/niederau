#!/usr/bin/env python3
"""Genereert de losse pagina 'Markbachjoch' in NL, EN en DE (inclusief SEO/GEO-blok).
Bron van de tekst staat hier (per taal naast elkaar); draai via tools/build.sh."""
import datetime, html, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://niederau.nl"
TODAY = datetime.date.today().isoformat()
SLUG = "markbachjoch"
LANGS = ("nl", "en", "de")
OG_IMAGE = f"{BASE}/assets/img/niederau-wildschoenau-tirol-1200x630.jpg"


def t(nl, en, de):
    return {"nl": nl, "en": en, "de": de}


def url(lang):
    return f"{BASE}/{SLUG}/" if lang == "nl" else f"{BASE}/{lang}/{SLUG}/"


TITLE = t("Markbachjoch Niederau: gondel, hutten en geschiedenis",
          "Markbachjoch Niederau: gondola, mountain huts and history",
          "Markbachjoch Niederau: Gondel, Hütten und Geschichte")
DESC = t("Het Markbachjoch boven Niederau: de Markbachjochbahn, hutten en restaurants, wandelen, skiën en de geschiedenis sinds de eerste stoeltjeslift van 1947.",
         "The Markbachjoch above Niederau: the gondola, mountain huts and restaurants, hiking, skiing and history since the first chairlift of 1947.",
         "Das Markbachjoch über Niederau: Markbachjochbahn, Hütten und Gasthäuser, Wandern, Skifahren und Geschichte seit dem ersten Sessellift von 1947.")
OG_TITLE = t("Markbachjoch – de oudste bergbaan van Niederau", "Markbachjoch – Niederau’s oldest mountain lift", "Markbachjoch – die älteste Bergbahn von Niederau")
IMG_ALT = t("Gondel van de Markbachjochbahn boven Niederau", "Gondola of the Markbachjochbahn above Niederau", "Gondel der Markbachjochbahn über Niederau")

FAQ = [
    (t("Hoe lang duurt de rit met de Markbachjochbahn?", "How long is the ride on the Markbachjochbahn?", "Wie lange dauert die Fahrt mit der Markbachjochbahn?"),
     t("De achtpersoons gondel van Niederau naar het Markbachjoch doet er ongeveer zes minuten over. De oude stoeltjeslift had er rond de achttien minuten voor nodig.",
       "The eight-seater gondola from Niederau to the Markbachjoch takes about six minutes. The old chairlift needed around eighteen minutes.",
       "Die Acht-Personen-Gondel von Niederau zum Markbachjoch braucht etwa sechs Minuten. Der alte Sessellift brauchte rund achtzehn Minuten.")),
    (t("Is het Markbachjoch ook in de zomer toegankelijk?", "Can you visit the Markbachjoch in summer too?", "Ist das Markbachjoch auch im Sommer zugänglich?"),
     t("Ja. De gondel rijdt ook in het zomerseizoen en brengt wandelaars, gezinnen en paraglidepiloten naar boven. Begin en einde van het seizoen en de dagelijkse tijden wisselen per jaar; kijk bij de Wildschönauer Bergbahnen voor de actuele tijden.",
       "Yes. The gondola also runs in the summer season and takes hikers, families and paraglider pilots up. The start and end of the season and daily times change from year to year; check the Wildschönauer Bergbahnen for current times.",
       "Ja. Die Gondel fährt auch in der Sommersaison und bringt Wanderer, Familien und Gleitschirmpiloten hinauf. Saisonbeginn, Saisonende und Betriebszeiten wechseln von Jahr zu Jahr; aktuelle Zeiten gibt es bei den Wildschönauer Bergbahnen.")),
    (t("Welke hutten en restaurants zijn er bij het Markbachjoch?", "Which huts and restaurants are there at the Markbachjoch?", "Welche Hütten und Gasthäuser gibt es am Markbachjoch?"),
     t("Vlak bij het bergstation vind je de Rübezahl-Hütte en de Markbachjochalm; bij het dalstation staat de Schnapshütte. Iets verder lopend ligt de Norderbergalm. Openingstijden wisselen per seizoen, dus controleer ze vooraf.",
       "Close to the top station you will find the Rübezahl-Hütte and the Markbachjochalm; the Schnapshütte stands at the valley station. A short walk further is the Norderbergalm. Opening times change with the season, so check ahead.",
       "Nahe der Bergstation liegen die Rübezahl-Hütte und die Markbachjochalm; an der Talstation steht die Schnapshütte. Etwas weiter zu Fuß liegt die Norderbergalm. Die Öffnungszeiten wechseln je nach Saison, bitte vorher prüfen.")),
    (t("Wat is de geschiedenis van het Markbachjoch?", "What is the history of the Markbachjoch?", "Was ist die Geschichte des Markbachjochs?"),
     t("Hier opende op 14 januari 1947 de eerste stoeltjeslift van Tirol, gebouwd door ingenieur Sepp Hochmuth. In 1995 kwam er een gondelbaan voor acht personen voor in de plaats.",
       "Here the first chairlift in Tyrol opened on 14 January 1947, built by engineer Sepp Hochmuth. In 1995 an eight-seater gondola replaced it.",
       "Hier wurde am 14. Januar 1947 der erste Sessellift Tirols eröffnet, gebaut von Ingenieur Sepp Hochmuth. 1995 ersetzte ihn eine Acht-Personen-Gondel.")),
]

L = {
 "home": t("Niederau", "Niederau", "Niederau"),
 "skip": t("Naar de inhoud", "Skip to content", "Zum Inhalt"),
 "menu": t("Menu", "Menu", "Menü"),
 "nav_label": t("Hoofdmenu", "Main menu", "Hauptmenü"),
 "n_home": t("Het dorp", "The village", "Das Dorf"),
 "n_lifts": t("Liften", "Lifts", "Lifte"),
 "n_food": t("Hutten & restaurants", "Huts & restaurants", "Hütten & Gasthäuser"),
 "n_hist": t("Geschiedenis", "History", "Geschichte"),
 "n_season": t("Zomer & winter", "Summer & winter", "Sommer & Winter"),
 "toggle_label": t("Wissel tussen zomer- en winterversie", "Switch between summer and winter version", "Zwischen Sommer- und Winterversion wechseln"),
 "toggle_s": t("☀ Zomer", "☀ Summer", "☀ Sommer"),
 "toggle_w": t("❄ Winter", "❄ Winter", "❄ Winter"),
 "lang_label": t("Taal", "Language", "Sprache"),
 "back": t("← Terug naar Niederau", "← Back to Niederau", "← Zurück zu Niederau"),
 "eyebrow": t("Bergbaan van Niederau", "Niederau’s mountain lift", "Bergbahn von Niederau"),
 "h1": t("Het Markbachjoch", "The Markbachjoch", "Das Markbachjoch"),
 "lead": t("Vanuit het dorp zie je hem al: het Markbachjoch, de berg waar in 1947 de eerste stoeltjeslift van Tirol naartoe ging. Tot vandaag is hij het uithangbord van Niederau, in de winter voor skiërs en in de zomer voor wandelaars, gezinnen en paragliders.",
           "You can see it from the village: the Markbachjoch, the mountain that got the first chairlift in Tyrol in 1947. To this day it is Niederau’s showpiece – for skiers in winter, for hikers, families and paragliders in summer.",
           "Man sieht es schon vom Dorf aus: das Markbachjoch, der Berg, auf den 1947 der erste Sessellift Tirols führte. Bis heute ist es das Aushängeschild von Niederau – im Winter für Skifahrer, im Sommer für Wanderer, Familien und Gleitschirmflieger."),
 "f1": t("± 1.500 m", "± 1,500 m", "± 1.500 m"), "f1t": t("hoogte van het Markbachjoch (top circa 1.496 m)", "height of the Markbachjoch (summit about 1,496 m)", "Höhe des Markbachjochs (Gipfel rund 1.496 m)"),
 "f2": t("± 6 min", "± 6 min", "± 6 Min."), "f2t": t("rit met de gondel vanuit het dorp", "gondola ride from the village", "Fahrt mit der Gondel vom Dorf"),
 "f3": t("1947", "1947", "1947"), "f3t": t("opening van de eerste stoeltjeslift van Tirol", "the first chairlift in Tyrol opens", "Eröffnung des ersten Sessellifts Tirols"),
 "f4": t("8 personen", "8 people", "8 Personen"), "f4t": t("per cabine in de huidige gondel (sinds 1995)", "per cabin in today’s gondola (since 1995)", "pro Kabine in der heutigen Gondel (seit 1995)"),
 "lifts_e": t("Liften", "Lifts", "Lifte"), "lifts_h": t("De Markbachjochbahn en de liften erom heen", "The Markbachjochbahn and the lifts around it", "Die Markbachjochbahn und die Lifte rundherum"),
 "lifts_p1": t("De Markbachjochbahn vertrekt aan de rand van Niederau en brengt je in ongeveer zes minuten naar het Markbachjoch. Het is een gondelbaan met cabines voor acht personen, gebouwd door Doppelmayr in 1995. Volgens de gegevens van skiresort.info kan de baan ongeveer 1.200 personen per uur vervoeren.",
               "The Markbachjochbahn starts at the edge of Niederau and takes you to the Markbachjoch in about six minutes. It is a gondola with eight-person cabins, built by Doppelmayr in 1995. According to skiresort.info, it can carry roughly 1,200 people per hour.",
               "Die Markbachjochbahn startet am Rand von Niederau und bringt dich in etwa sechs Minuten aufs Markbachjoch. Es ist eine Gondelbahn mit Acht-Personen-Kabinen, 1995 von Doppelmayr gebaut. Laut skiresort.info kann sie etwa 1.200 Personen pro Stunde befördern."),
 "lifts_p2": t("Boven sluit het skigebied aan op het lift- en pistenetwerk van Ski Juwel Alpbachtal Wildschönau. Aan de overkant van het dorp ligt het Lanerköpfl, het tweede, wat rustigere deel van het skigebied van Niederau. Rond het bergstation is volgens skiresort.info een overdekte loopband voor skiërs aangekondigd; check de actuele stand bij de Wildschönauer Bergbahnen.",
               "At the top, the ski area connects to the lift and piste network of Ski Juwel Alpbachtal Wildschönau. Across the village lies the Lanerköpfl, the second, somewhat quieter part of Niederau’s ski area. Around the top station a covered moving carpet for skiers has been announced; check the current status with the Wildschönauer Bergbahnen.",
               "Oben schließt das Skigebiet an das Lift- und Pistennetz des Ski Juwel Alpbachtal Wildschönau an. Auf der anderen Seite des Dorfes liegt das Lanerköpfl, der zweite, etwas ruhigere Teil des Skigebiets von Niederau. Rund um die Bergstation wurde ein überdachtes Förderband für Skifahrer angekündigt; den aktuellen Stand erfährst du bei den Wildschönauer Bergbahnen."),
 "lifts_link": t("Meer over het Lanerköpfl", "More about the Lanerköpfl", "Mehr zum Lanerköpfl"),
 "lifts_bahn": t("Wildschönauer Bergbahnen", "Wildschönauer Bergbahnen", "Wildschönauer Bergbahnen"),
 "food_e": t("Hutten & restaurants", "Huts & restaurants", "Hütten & Gasthäuser"), "food_h": t("Eten en drinken op de berg", "Eating and drinking on the mountain", "Essen und Trinken am Berg"),
 "food_intro": t("Rond het Markbachjoch liggen meerdere plekken om te pauzeren. Openingstijden verschillen per seizoen; bel of kijk op de website voordat je erheen gaat.",
                 "There are several places to stop around the Markbachjoch. Opening times differ by season; call or check the website before you go.",
                 "Rund ums Markbachjoch gibt es mehrere Einkehrmöglichkeiten. Die Öffnungszeiten unterscheiden sich je nach Saison; ruf an oder schau auf die Website, bevor du aufsteigst."),
 "c1h": t("Rübezahl-Hütte", "Rübezahl-Hütte", "Rübezahl-Hütte"),
 "c1p": t("Panoramaberggasthof met een groot zonneterras, vlak bij het bergstation. Je bereikt hem met de gondel. Op zondag is er volgens de toeristische bronnen vaak live volksmuziek.",
          "Panorama mountain inn with a large sun terrace, close to the top station. You get there by gondola. According to tourist sources there is often live folk music on Sundays.",
          "Panorama-Berggasthof mit großer Sonnenterrasse, nahe der Bergstation. Du erreichst ihn mit der Gondel. Laut Tourismusquellen gibt es sonntags oft Live-Volksmusik."),
 "c1l": t("Rübezahl-Hütte bij Ski Juwel", "Rübezahl-Hütte at Ski Juwel", "Rübezahl-Hütte bei Ski Juwel"),
 "c2h": t("Markbachjochalm", "Markbachjochalm", "Markbachjochalm"),
 "c2p": t("Alm bij het Markbachjoch die goed bij gezinnen past: er zijn een speeltuin en een kleine dierenweide, en bij mooi weer hangmatten om even uit te rusten.",
          "Alpine hut at the Markbachjoch that suits families: there is a playground and a small petting zoo, and in good weather hammocks for a rest.",
          "Alm am Markbachjoch, die gut zu Familien passt: Es gibt einen Spielplatz und einen kleinen Streichelzoo, bei schönem Wetter auch Hängematten zum Ausruhen."),
 "c3h": t("Schnapshütte", "Schnapshütte", "Schnapshütte"),
 "c3p": t("Snackbar aan het dalstation van de Markbachjochbahn: handig voor een hapje of een drankje voor of na de rit, zeker na een dag op de piste.",
          "Snack bar at the valley station of the Markbachjochbahn: handy for a bite or a drink before or after the ride, especially after a day on the slopes.",
          "Snackbar an der Talstation der Markbachjochbahn: praktisch für eine Kleinigkeit oder ein Getränk vor oder nach der Fahrt, besonders nach einem Tag auf der Piste."),
 "c3l": t("Schnapshütte bij Ski Juwel", "Schnapshütte at Ski Juwel", "Schnapshütte bei Ski Juwel"),
 "c4h": t("Norderbergalm", "Norderbergalm", "Norderbergalm"),
 "c4p": t("Gezellige alm op ongeveer 1.360 meter, circa een half uur lopen vanaf het bergstation. Er zijn Tiroler gerechten en zelfgemaakte taart. Ook rond het Lanerköpfl, bijvoorbeeld bij de Holzalm, kun je goed pauzeren.",
          "Cosy alpine hut at about 1,360 metres, roughly half an hour’s walk from the top station. It serves Tyrolean dishes and homemade cake. Around the Lanerköpfl too, for example at the Holzalm, there are good places to stop.",
          "Gemütliche Alm auf etwa 1.360 Metern, rund eine halbe Gehstunde von der Bergstation. Es gibt Tiroler Gerichte und selbstgebackenen Kuchen. Auch rund ums Lanerköpfl, etwa bei der Holzalm, lässt es sich gut einkehren."),
 "photo_food": t("Brettljause, een plank met Tiroler vleeswaren en kaas, op een alm", "Brettljause, a Tyrolean board of cured meats and cheese, at an alpine hut", "Brettljause, eine Tiroler Jausenplatte, auf einer Alm"),
 "hist_e": t("Geschiedenis", "History", "Geschichte"), "hist_h": t("De eerste stoeltjeslift van Tirol", "The first chairlift in Tyrol", "Der erste Sessellift Tirols"),
 "hist_p1": t("Het begon na de oorlog. In 1946 startte ingenieur Sepp Hochmuth, een opgeleid machinebankwerker, met de bouw van een stoeltjeslift van Niederau naar het Markbachjoch. Het was een echte zelfbouw: voor de zitjes gebruikte men volgens de overlevering dunne houten planken, draden en waterleidingbuizen, en een oude tankmotor leverde de aandrijving.",
              "It began after the war. In 1946 engineer Sepp Hochmuth, a trained machine fitter, started building a chairlift from Niederau to the Markbachjoch. It was a true do-it-yourself project: according to tradition, thin wooden boards, wires and water pipes were used for the seats, and an old tank engine supplied the drive.",
              "Es begann nach dem Krieg. 1946 begann Ingenieur Sepp Hochmuth, ein ausgebildeter Maschinenschlosser, mit dem Bau eines Sessellifts von Niederau aufs Markbachjoch. Es war ein echter Eigenbau: Für die Sitze verwendete man der Überlieferung nach dünne Holzbretter, Drähte und Wasserleitungsrohre, und ein alter Panzermotor lieferte den Antrieb."),
 "hist_p2": t("Op 14 januari 1947 ging de lift open. Daarmee kreeg het dal zijn eerste bergbaan en begon het wintertoerisme in de Wildschönau. Wie vandaag in de gondel stapt, volgt dus nog steeds de lijn van die eerste lift.",
              "The lift opened on 14 January 1947. It gave the valley its first mountain lift and marked the start of winter tourism in the Wildschönau. Anyone stepping into the gondola today still follows the line of that first lift.",
              "Am 14. Januar 1947 ging der Lift in Betrieb. Damit bekam das Tal seine erste Bergbahn, und der Wintertourismus in der Wildschönau begann. Wer heute in die Gondel steigt, folgt noch immer der Linie dieses ersten Lifts."),
 "t1": t("1946", "1946", "1946"), "t1t": t("Ingenieur Sepp Hochmuth begint met de bouw van de stoeltjeslift naar het Markbachjoch.", "Engineer Sepp Hochmuth starts building the chairlift to the Markbachjoch.", "Ingenieur Sepp Hochmuth beginnt mit dem Bau des Sessellifts aufs Markbachjoch."),
 "t2": t("14 januari 1947", "14 January 1947", "14. Januar 1947"), "t2t": t("Opening van de lift, volgens de overlevering de eerste stoeltjeslift van Tirol.", "The lift opens – by tradition the first chairlift in Tyrol.", "Eröffnung des Lifts, der Überlieferung nach der erste Sessellift Tirols."),
 "t3": t("1972", "1972", "1972"), "t3t": t("Een nieuwe tweepersoons stoeltjeslift (Swoboda) neemt het over.", "A new two-person chairlift (Swoboda) takes over.", "Ein neuer Zweier-Sessellift (Swoboda) übernimmt."),
 "t4": t("1995", "1995", "1995"), "t4t": t("De gondelbaan voor acht personen (Doppelmayr) vervangt de stoeltjeslift: de huidige Markbachjochbahn.", "The eight-person gondola (Doppelmayr) replaces the chairlift: today’s Markbachjochbahn.", "Die Acht-Personen-Gondel (Doppelmayr) ersetzt den Sessellift: die heutige Markbachjochbahn."),
 "t5": t("2022", "2022", "2022"), "t5t": t("De bergbaan in Niederau viert haar 75-jarig jubileum.", "Niederau’s mountain lift celebrates its 75th anniversary.", "Die Bergbahn in Niederau feiert ihr 75-jähriges Jubiläum."),
 "hist_more": t("Meer geschiedenis van het dorp", "More history of the village", "Mehr Geschichte des Dorfes"),
 "photo_hist": t("Gondel van de Markbachjochbahn boven Niederau met uitzicht over de Alpen", "Gondola of the Markbachjochbahn above Niederau with a view over the Alps", "Gondel der Markbachjochbahn über Niederau mit Blick über die Alpen"),
 "s_e": t("Zomer & winter", "Summer & winter", "Sommer & Winter"), "s_h": t("Wat doe je op het Markbachjoch?", "What to do on the Markbachjoch", "Was kann man am Markbachjoch unternehmen?"),
 "w_h": t("In de winter", "In winter", "Im Winter"),
 "w_p": t("Brede, zonnige pistes boven het dorp, geschikt voor beginners, gezinnen en wie rustig wil skiën. Terug naar Niederau kan op de piste. Op de noordhellingen vind je pittiger afdalingen, zoals de Hochberg-afdaling. Voor de allerkleinsten zijn er oefenweides bij het dorp; vraag naar de actuele situatie van de oefenlift.",
          "Wide, sunny slopes above the village, suitable for beginners, families and relaxed skiing. You can ski back down to Niederau. The north-facing slopes have steeper runs, such as the Hochberg run. For the youngest there are practice slopes near the village; ask about the current status of the practice lift.",
          "Breite, sonnige Pisten über dem Dorf, geeignet für Anfänger, Familien und gemütliches Skifahren. Zurück nach Niederau geht es auf der Piste. An den Nordhängen gibt es steilere Abfahrten, etwa die Hochberg-Abfahrt. Für die Kleinsten gibt es Übungswiesen beim Dorf; fragen Sie nach dem aktuellen Stand des Übungslifts."),
 "su_h": t("In de zomer", "In summer", "Im Sommer"),
 "su_p": t("Met de gondel sla je de klim over en begin je meteen op de bergweiden. Populaire routes lopen naar de Rosskopf via de Halsgatterl of naar de Feldalphorn, en er is een rustiger pad langs de bosrand naar Penningdörfl met uitzicht tot de Hohe Salve en de Wilder Kaiser. Het Markbachjoch is ook een bekende startplaats voor paragliders; de startplek ligt onder de hut. Gezinnen vinden bij de alm een speeltuin en dieren.",
           "The gondola lets you skip the climb and start straight on the mountain pastures. Popular routes lead to the Rosskopf via the Halsgatterl or to the Feldalphorn, and there is a quieter path along the forest edge to Penningdörfl with views to the Hohe Salve and the Wilder Kaiser. The Markbachjoch is also a well-known take-off site for paragliders; the launch area lies below the hut. Families will find a playground and animals at the alpine hut.",
           "Mit der Gondel sparst du dir den Aufstieg und bist gleich auf den Bergwiesen. Beliebte Touren führen zum Rosskopf über das Halsgatterl oder zum Feldalphorn, und ein ruhigerer Weg am Waldrand führt nach Penningdörfl mit Blick bis zur Hohen Salve und zum Wilden Kaiser. Das Markbachjoch ist auch ein bekannter Startplatz für Gleitschirmflieger; der Startplatz liegt unterhalb der Hütte. Familien finden bei der Alm einen Spielplatz und Tiere."),
 "photo_w": t("Skiërs op de zonnige pistes van het Markbachjoch boven Niederau", "Skiers on the sunny slopes of the Markbachjoch above Niederau", "Skifahrer auf den sonnigen Pisten des Markbachjochs über Niederau"),
 "photo_s": t("Wandelpad door de weiden naar de alm", "Footpath through the meadows to the alpine hut", "Wanderweg über die Wiesen zur Alm"),
 "faq_e": t("Vragen", "Questions", "Fragen"), "faq_h": t("Veelgestelde vragen over het Markbachjoch", "Frequently asked questions about the Markbachjoch", "Häufige Fragen zum Markbachjoch"),
 "tip": t("Let op: tijden, prijzen en seizoensdata veranderen. Controleer ze altijd bij de Wildschönauer Bergbahnen en bij de hutten zelf. Bronnen voor de geschiedenis en techniek: Wildschönau Tourismus, skiresort.info en de website van Ski Juwel.",
          "Please note: times, prices and season dates change. Always check them with the Wildschönauer Bergbahnen and the huts themselves. Sources for history and technical data: Wildschönau Tourismus, skiresort.info and the Ski Juwel website.",
          "Bitte beachten: Zeiten, Preise und Saisondaten ändern sich. Prüfe sie immer bei den Wildschönauer Bergbahnen und bei den Hütten selbst. Quellen für Geschichte und Technik: Wildschönau Tourismus, skiresort.info und die Website von Ski Juwel."),
 "f_about": t("Onafhankelijke gids over Niederau in de Wildschönau, Tirol.", "Independent guide to Niederau in the Wildschönau, Tyrol.", "Unabhängiger Reiseführer zu Niederau in der Wildschönau, Tirol."),
 "f_back": t("Terug naar de hoofdpagina", "Back to the main page", "Zurück zur Hauptseite"),
 "copy": t("Onafhankelijke site, niet verbonden aan officiële instanties.", "Independent site, not affiliated with official bodies.", "Unabhängige Seite, nicht mit offiziellen Stellen verbunden."),
 "credits": t("Foto’s: Wildschönau Tourismus, Ski Juwel Alpbachtal Wildschönau, Wildschönauer Bergbahnen, Hotel Wastlhof en eigen foto’s.",
              "Photos: Wildschönau Tourismus, Ski Juwel Alpbachtal Wildschönau, Wildschönauer Bergbahnen, Hotel Wastlhof and own photos.",
              "Fotos: Wildschönau Tourismus, Ski Juwel Alpbachtal Wildschönau, Wildschönauer Bergbahnen, Hotel Wastlhof und eigene Fotos."),
}
# ankers op de hoofdpagina verschillen per taal
HOME_ANCHOR = {"geschiedenis": t("geschiedenis", "history", "geschichte"),
               "lanerkoepfl": t("lanerkoepfl", "lanerkoepfl", "lanerkoepfl"),
               "seizoenen": t("seizoenen", "seasons", "jahreszeiten")}
LINKS = {
    "bahn": "https://www.wildschoenau.com/",
    "ruebezahl": "https://www.skijuwel.com/en/summer/mountain-huts/Rubezahl-Hut_isd_89913",
    "schnaps": "https://www.skijuwel.com/en/winter/huts-and-restaurants/Schnapshutte-Niederau_isd_88696",
}


def main_nav(lang):
    """Zelfde hoofdmenu als de hoofdpagina (uit de gebouwde index van die taal)."""
    import re
    pre_ = "" if lang == "nl" else lang + "/"
    t_ = (ROOT / (pre_ + "index.html")).read_text(encoding="utf-8")
    nav = t_[t_.index('<nav class="nav"'):t_.index('<button class="season-toggle"')]
    home_ = "/" if lang == "nl" else f"/{lang}/"
    out = []
    for href, label in re.findall(r'<a href="([^"]+)">([^<]+)</a>', nav):
        url_ = f"{home_}{href}" if href.startswith("#") else f"/{pre_}{href}"
        out.append(f'<a href="{url_}">{label}</a>')
    return "\n      ".join(out)


def render(lang):
    g = lambda k: L[k][lang]
    e = html.escape
    pre = "../" if lang == "nl" else "../../"           # pad naar assets
    home = "../"                                        # NL: /, EN/DE: /en/ resp. /de/
    here = url(lang)
    lang_links = {
        "nl": "./" if lang == "nl" else "../../markbachjoch/",
        "en": "../en/markbachjoch/" if lang == "nl" else ("./" if lang == "en" else "../../en/markbachjoch/"),
        "de": "../de/markbachjoch/" if lang == "nl" else ("./" if lang == "de" else "../../de/markbachjoch/"),
    }
    cur = lambda c: ' aria-current="true"' if c == lang else ''
    lang_nav = "".join(
        f'<a href="{lang_links[c]}" hreflang="{c}" lang="{c}"{cur(c)}>{c.upper()}</a>' for c in LANGS)
    anchor = lambda k: HOME_ANCHOR[k][lang]
    faq_html = "\n".join(f'      <details>\n        <summary>{e(q[lang])}</summary>\n        <p>{e(a[lang])}</p>\n      </details>' for q, a in FAQ)
    faq_ld = [{"@type": "Question", "name": q[lang], "acceptedAnswer": {"@type": "Answer", "text": a[lang]}} for q, a in FAQ]
    graph = [
        {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/", "name": "Niederau.nl", "inLanguage": ["nl", "en", "de"]},
        {"@type": "WebPage", "@id": here + "#webpage", "url": here, "name": TITLE[lang], "description": DESC[lang],
         "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#website"}, "about": {"@id": here + "#markbachjoch"},
         "dateModified": TODAY, "breadcrumb": {"@id": here + "#breadcrumb"},
         "primaryImageOfPage": {"@type": "ImageObject", "url": f"{BASE}/assets/img/niederau-markbachjochbahn-gondel.webp"}},
        {"@type": "BreadcrumbList", "@id": here + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Niederau", "item": f"{BASE}/" if lang == "nl" else f"{BASE}/{lang}/"},
            {"@type": "ListItem", "position": 2, "name": g("h1"), "item": here}]},
        {"@type": ["TouristAttraction", "Place"], "@id": here + "#markbachjoch", "name": "Markbachjoch",
         "description": DESC[lang], "image": f"{BASE}/assets/img/niederau-markbachjochbahn-gondel.webp",
         "geo": {"@type": "GeoCoordinates", "elevation": 1496},
         "address": {"@type": "PostalAddress", "streetAddress": "Markbachjoch 84", "postalCode": "6314",
                     "addressLocality": "Wildschönau", "addressRegion": "Tirol", "addressCountry": "AT"},
         "containedInPlace": {"@type": "TouristDestination", "name": "Niederau, Wildschönau, Tirol, Austria"}},
        {"@type": "FAQPage", "@id": here + "#faq", "inLanguage": lang, "mainEntity": faq_ld},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    hreflangs = "\n".join(f'<link rel="alternate" hreflang="{c}" href="{url(c)}">' for c in LANGS) + f'\n<link rel="alternate" hreflang="x-default" href="{url("en")}">'
    locale = {"nl": "nl_NL", "en": "en_GB", "de": "de_DE"}[lang]
    toggle = f'<button class="season-toggle" type="button" aria-label="{e(g("toggle_label"))}" title="{e(g("toggle_label"))}"><span data-only="winter">{g("toggle_s")}</span><span data-only="summer">{g("toggle_w")}</span></button>'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(TITLE[lang])}</title>
<meta name="description" content="{e(DESC[lang])}">
<link rel="canonical" href="{here}">
{hreflangs}
<meta property="og:type" content="article">
<meta property="og:locale" content="{locale}">
<meta property="og:title" content="{e(OG_TITLE[lang])}">
<meta property="og:description" content="{e(DESC[lang])}">
<meta property="og:url" content="{here}">
<meta name="theme-color" content="#efece7">
<!-- SEO:START (gegenereerd door tools/subpages.py) -->
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="AT-7">
<meta name="geo.placename" content="Markbachjoch, Niederau, Wildschönau, Tirol, Austria">
<meta name="geo.position" content="47.4446;12.0789">
<meta name="ICBM" content="47.4446, 12.0789">
<meta property="og:site_name" content="Niederau.nl">
<meta property="og:image" content="{BASE}/assets/img/niederau-markbachjochbahn-gondel.webp">
<meta property="og:image:alt" content="{e(IMG_ALT[lang])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(OG_TITLE[lang])}">
<meta name="twitter:description" content="{e(DESC[lang])}">
<meta name="twitter:image" content="{BASE}/assets/img/niederau-markbachjochbahn-gondel.webp">
<script type="application/ld+json">
{ld}
</script>
<!-- SEO:END -->
<link rel="icon" href="{pre}assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{pre}assets/favicon-48.png" sizes="48x48" type="image/png">
<link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="stylesheet" href="{pre}assets/style.css">
<script>
  (function () {{
    var m = new Date().getMonth(), season = (m >= 9 || m <= 2) ? 'winter' : 'summer';
    document.documentElement.setAttribute('data-season', season);
  }})();
</script>
</head>
<body>
<a class="skip" href="#main">{g("skip")}</a>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{home}">
      <svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#b5222b"/><circle cx="46" cy="18" r="7" fill="#f5d27a"/><path d="M4 52 22 24l9 12 8-10 21 26z" fill="#fbfaf6"/></svg>
      <span>Niederau<small>Wildschönau · {"Tirol" if lang != "en" else "Tyrol"}</small></span>
    </a>
    <button class="menu-btn" aria-expanded="false" aria-controls="nav">{g("menu")}</button>
    <nav class="nav" id="nav" aria-label="{g("nav_label")}">
      {main_nav(lang)}
      {toggle}
      <div class="lang" aria-label="{g("lang_label")}">
        {lang_nav}
      </div>
    </nav>
  </div>
</header>

<main id="main">
<section class="page-hero" aria-hidden="true"></section>

<section aria-labelledby="h-top">
  <div class="wrap split">
    <div>
      <p class="breadcrumb"><a href="{home}">{g("back")}</a></p>
      <p class="eyebrow">{g("eyebrow")}</p>
      <h1 id="h-top">{g("h1")}</h1>
      <p>{g("lead")}</p>
    </div>
    <ul class="facts" aria-label="{g("h1")}">
      <li><strong>{g("f1")}</strong><span>{g("f1t")}</span></li>
      <li><strong>{g("f2")}</strong><span>{g("f2t")}</span></li>
      <li><strong>{g("f3")}</strong><span>{g("f3t")}</span></li>
      <li><strong>{g("f4")}</strong><span>{g("f4t")}</span></li>
    </ul>
  </div>
</section>

<section class="alt" id="liften" aria-labelledby="h-liften">
  <div class="wrap split" style="align-items:start">
    <div>
      <p class="eyebrow">{g("lifts_e")}</p>
      <h2 id="h-liften">{g("lifts_h")}</h2>
      <p>{g("lifts_p1")}</p>
      <p>{g("lifts_p2")}</p>
      <p><a href="{home}#{anchor("lanerkoepfl")}">{g("lifts_link")} →</a> · <a href="{LINKS["bahn"]}" rel="noopener" target="_blank">{g("lifts_bahn")}</a></p>
    </div>
    <img class="side-img" src="{pre}assets/img/niederau-markbachjochbahn-gondel.webp" width="1000" height="667" alt="{e(g("photo_hist"))}">
  </div>
</section>

<section id="eten" aria-labelledby="h-eten">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">{g("food_e")}</p>
      <h2 id="h-eten">{g("food_h")}</h2>
      <p>{g("food_intro")}</p>
    </div>
    <div class="grid grid-two">
      <article class="card"><h3>{g("c1h")}</h3><p>{g("c1p")}</p><p><a href="{LINKS["ruebezahl"]}" rel="noopener" target="_blank">{g("c1l")}</a></p></article>
      <article class="card"><h3>{g("c2h")}</h3><p>{g("c2p")}</p></article>
      <article class="card"><h3>{g("c3h")}</h3><p>{g("c3p")}</p><p><a href="{LINKS["schnaps"]}" rel="noopener" target="_blank">{g("c3l")}</a></p></article>
      <article class="card"><h3>{g("c4h")}</h3><p>{g("c4p")}</p></article>
    </div>
  </div>
</section>

<section class="alt" id="geschiedenis" aria-labelledby="h-hist">
  <div class="wrap split" style="align-items:start">
    <div>
      <p class="eyebrow">{g("hist_e")}</p>
      <h2 id="h-hist">{g("hist_h")}</h2>
      <p>{g("hist_p1")}</p>
      <p>{g("hist_p2")}</p>
      <p><a href="{home}#{anchor("geschiedenis")}">{g("hist_more")} →</a></p>
    </div>
    <ol class="timeline">
      <li><span class="when">{g("t1")}</span><br>{g("t1t")}</li>
      <li><span class="when">{g("t2")}</span><br>{g("t2t")}</li>
      <li><span class="when">{g("t3")}</span><br>{g("t3t")}</li>
      <li><span class="when">{g("t4")}</span><br>{g("t4t")}</li>
      <li><span class="when">{g("t5")}</span><br>{g("t5t")}</li>
    </ol>
  </div>
</section>

<section id="seizoenen" aria-labelledby="h-seizoenen">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">{g("s_e")}</p>
      <h2 id="h-seizoenen">{g("s_h")}</h2>
    </div>
    <div class="grid grid-two">
      <article class="card has-img">
        <img class="card-img" src="{pre}assets/img/niederau-skien-markbachjoch.webp" width="800" height="450" loading="lazy" alt="{e(g("photo_w"))}">
        <h3>{g("w_h")}</h3><p>{g("w_p")}</p>
      </article>
      <article class="card has-img">
        <img class="card-img" src="{pre}assets/img/wildschoenau-wandelpad-alm.webp" width="800" height="450" loading="lazy" alt="{e(g("photo_s"))}">
        <h3>{g("su_h")}</h3><p>{g("su_p")}</p>
      </article>
    </div>
  </div>
</section>

<section class="alt" id="faq" aria-labelledby="h-faq">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">{g("faq_e")}</p>
      <h2 id="h-faq">{g("faq_h")}</h2>
    </div>
    <div class="faq">
{faq_html}
    </div>
    <p class="note">{g("tip")}</p>
  </div>
</section>
</main>

<footer class="site-footer">
  <div class="wrap">
    <div>
      <h3>Niederau.nl</h3>
      <p>{g("f_about")}</p>
      <div class="lang" aria-label="{g("lang_label")}">
        {lang_nav}
      </div>
    </div>
    <div>
      <h3>Niederau</h3>
      <ul>
        <li><a href="{home}">{g("f_back")}</a></li>
        <li><a href="#liften">{g("n_lifts")}</a></li>
        <li><a href="#eten">{g("n_food")}</a></li>
        <li><a href="#geschiedenis">{g("n_hist")}</a></li>
      </ul>
    </div>
    <p class="credits">{g("credits")}</p>
    <p class="copyright">© <span data-year>{TODAY[:4]}</span> Niederau.nl · {g("copy")}</p>
  </div>
</footer>
<script src="{pre}assets/main.js" defer></script>
</body>
</html>
'''


def pages():
    out = {}
    for lang in LANGS:
        rel = f"{SLUG}/index.html" if lang == "nl" else f"{lang}/{SLUG}/index.html"
        out[lang] = rel
        p = ROOT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(render(lang), encoding="utf-8")
        print("Subpagina bijgewerkt:", rel)
    return out


if __name__ == "__main__":
    pages()
