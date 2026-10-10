<!--
Gegenereerd uit app/templates/seo/api_voorwaarden.html (app-repo, commit e0a1a0cf)
door scripts/maintenance/export_api_terms.py. Niet met de hand bewerken.
-->

> **Vervallen versie.** Dit is versie 1.10 van de API-voorwaarden, zoals die vanaf 30 september 2026
> op de site stond. Bindend is de huidige versie op <https://www.prijsprofeet.nl/api-voorwaarden>. Alle versies staan in
> [het overzicht](README.md).

# API-voorwaarden

Versie 1.10, 30 september 2026

> **Samenvatting.** Je mag onze data gebruiken om je eigen product te bouwen. Je mag er geen kopie van onze database mee opbouwen, de ruwe data niet doorverkopen, en na afloop van een proefperiode of abonnement verwijder je de opgeslagen data. Prijsdata is indicatief; controleer bij de retailer.

## 1. Wie zijn wij

De PrijsProfeet API wordt aangeboden door **Better Call Birdman**, eenmanszaak, ingeschreven bij de Kamer van Koophandel onder nummer **84948396** ("PrijsProfeet", "wij", "ons"). In deze voorwaarden ben jij ("je", "afnemer") de partij die de API gebruikt.

## 2. Waarop deze voorwaarden van toepassing zijn

Deze voorwaarden gelden voor **alle** toegang tot de API op `prijsprofeet.nl/api/v1/*` en `prijsprofeet.be/api/v1/*`, met of zonder API-key, betaald of gratis. Ze gelden niet voor het gewone gebruik van de website; daarvoor geldt onze [disclaimer](https://www.prijsprofeet.nl/disclaimer). Waar deze voorwaarden afwijken van de disclaimer, gaan deze voorwaarden voor als het om de API gaat.

Ons [privacybeleid](https://www.prijsprofeet.nl/privacy) geldt **wél voor allebei**: artikel 8 daarvan beschrijft precies welke gegevens we van API-afnemers verwerken en hoe lang we ze bewaren. Zie ook artikel 15 hieronder.

Je aanvaardt deze voorwaarden:

- **Gratis (zonder key):** door de API te gebruiken. Er is geen registratie, dus gebruik geldt als aanvaarding.
- **Gratis (met key):** door een gratis key aan te vragen op de [API-pagina](https://www.prijsprofeet.nl/api). Bij het formulier staat een link naar deze voorwaarden, en in de e-mail waarmee je de key ophaalt staat die opnieuw, zodat je ze kunt lezen vóórdat je de key hebt.
- **Proef, Pro en Business:** door de API-key in gebruik te nemen. We sturen deze voorwaarden mee met de e-mail waarin je de key ontvangt, vóórdat er een factuur volgt.

## 3. De plannen

| Plan | Toegang | Limiet | Commercieel gebruik | Bronvermelding | SLA |
|---|---|---|---|---|---|
| **Gratis** zonder key | Publieke endpoints, geen key nodig | 30–120 req/min **per endpoint**, per IP-adres | Ja | Verplicht | Nee |
| **Gratis** met key | Dezelfde endpoints; key gratis aan te vragen | 150 req/min **op je key** in plaats van je IP-adres | Ja | Verplicht | Nee |
| **Proef** | Alles uit Pro, tijdelijk | 300 req/min | Nee, alleen evaluatie | Verplicht | Nee |
| **Pro** | + `/match/*` en `/price-history` | 300 req/min | Ja | Niet nodig | Nee |
| **Business** | Alles uit Pro | tot 1.000 req/min | Ja | Niet nodig | Ja, zie artikel 10 |

Actuele prijzen staan op de [API-pagina](https://www.prijsprofeet.nl/api). Prijzen zijn exclusief btw.

**Over de limieten.** Zonder key tellen we per endpoint en per IP-adres; met een key tellen we op de key. Bouw je server-side, dan deelt je hele gebruikersbestand anders één IP-limiet. Dat is precies waarom de gratis key bestaat. De genoemde aantallen zijn de limieten die we vandaag hanteren; we kunnen ze aanpassen als de belasting daarom vraagt. Voor betalende afnemers doen we dat niet naar beneden zonder de aankondigingstermijn van artikel 16.

## 4. Je API-key

Een key is persoonlijk voor jou of je organisatie. Daarbij geldt:

- **Houd hem geheim.** Zet hem niet in client-side code, een publieke repository of een app die je uitlevert aan eindgebruikers. Wie de key heeft, kan hem gebruiken.
- **Verkeer onder jouw key rekenen we aan jou toe.** Ook als een ander hem gebruikt. Vermoed je dat je key is uitgelekt, vraag dan een nieuwe aan of laat het ons weten.
- **Een nieuwe key vervangt de oude.** Vraag je opnieuw een gratis key aan op hetzelfde e-mailadres, dan draaien we er een nieuwe voor je en stopt de oude direct met werken. We tonen een key **één keer**: we bewaren zelf alleen een hash en kunnen hem niet opnieuw laten zien.
- **Betaalde keys draaien we niet via het formulier.** Dat zou een lopende integratie kunnen breken. Neem daarvoor contact met ons op.
- **We kunnen een key intrekken** volgens artikel 12. Een ingetrokken key leeft niet vanzelf weer op door opnieuw een key aan te vragen.

## 5. Proefperiode

Op verzoek geven we een **proefperiode van 14 dagen** met Pro-functionaliteit, gratis en zonder betaalgegevens. Daarvoor gelden een paar extra regels:

- De proef is bedoeld om te **evalueren**, niet om er een product mee in productie te draaien of om er commercieel voordeel uit te halen.
- De proef loopt **automatisch af**. De key stopt op de einddatum met werken; wij hoeven niets op te zeggen en jij ook niet.
- Eén proefperiode per organisatie. Een proef gaat alleen over in een betaald plan als je daar expliciet mee instemt. Er wordt niets automatisch omgezet of afgeschreven.
- Tijdens de proef gelden geen beschikbaarheidsgaranties en is onze aansprakelijkheid uitgesloten voor zover de wet dat toestaat.

> **Verwijderplicht na afloop.** Binnen **14 dagen** na het einde van de proefperiode verwijder je alle via de API verkregen data uit je systemen, inclusief caches, kopieën, exports en back-ups voor zover technisch mogelijk. Je mag de data uit een proef dus niet houden of blijven gebruiken nadat de proef is afgelopen. Op ons verzoek bevestig je de verwijdering schriftelijk. Deze plicht geldt ook na beëindiging van een betaald plan (artikel 7).

## 6. Wat je met de data mag en niet mag

Zolang je plan loopt, geven we je een **niet-exclusief, niet-overdraagbaar en herroepbaar** recht om de data via de API op te vragen en te verwerken in je eigen product, dienst, onderzoek of interne tool.

Niet toegestaan is:

- **De dataset nabouwen.** Systematisch of grootschalig data onttrekken om (een substantieel deel van) onze database te reconstrueren, na te bouwen of te dupliceren.
- **Doorverkoop van ruwe data.** De data as-is doorverkopen, doorleveren of als eigen datafeed of API aanbieden. Een product bouwen dát op de data draait mag wel; de data zelf doorverkopen niet.
- **Limieten omzeilen.** Meerdere keys of accounts gebruiken, keys delen met derden, of langs de rate limits werken.
- **Suggereren dat een supermarkt erachter zit.** Wij zijn onafhankelijk en hebben geen band met de genoemde ketens; presenteer de data niet als afkomstig van of goedgekeurd door een retailer.
- Gebruik dat in strijd is met de wet of dat de dienst, de infrastructuur of andere gebruikers schaadt.

**Waar de grens bij “nabouwen” ligt.** Die gaat over *hoe je ophaalt*, niet over *hoeveel je bewaart*.

- **De lopende aanbiedingen synchroniseren mag.** Je mag de acties die nu lopen of binnenkort beginnen regelmatig in hun geheel ophalen via de lijst-endpoints (`/api/v1/products` en `/api/v1/search`), pagina voor pagina, per keten of alles tegelijk, om je product actueel te houden. Daar zijn die endpoints voor. De acties worden eens per nacht bijgewerkt, dus een paar keer per dag ophalen is ruim voldoende.
- **Opvragen wat je gebruikers of je product nodig hebben** is normaal gebruik, ook als er na een jaar veel ligt, en ook als het schapprijzen zijn en niet alleen aanbiedingen.
- **De catalogus product voor product aflopen mag niet.** Alle producten of alle EAN's op rij opvragen, ongeacht of iemand ernaar vroeg, is het onttrekken uit de eerste regel hierboven, ook als het er weinig zijn. Voorbeelden zijn elk product-id langs `/api/v1/products/{id}` of elke EAN langs de zoek- of match-endpoints. Wil je alle lopende acties, gebruik dan de lijst-endpoints uit het eerste punt.

Wat je uit normaal gebruik hebt bewaard mag je houden en tonen zolang je plan loopt; artikel 7 zegt wat er bij het einde van je plan mee gebeurt.

**Bronvermelding, alleen voor Gratis en Proef.** Gebruik je de API zonder key of tijdens een proefperiode, en zien jouw gebruikers de data, dan vermeld je zichtbaar **PrijsProfeet** als bron met een link naar `prijsprofeet.nl`, op elk scherm of elke pagina waar die data staat. Wie niets betaalt, betaalt in bronvermelding.

**Pro en Business zijn hiervan vrijgesteld**: je mag de data zonder bronvermelding in je eigen product verwerken.

## 7. Caching, opslag en verwijdering

Je mag data cachen en opslaan zolang je plan loopt; dat hoort bij normaal gebruik. Prijzen veranderen wekelijks: cache prijsdata niet langer dan 24 uur, zodat je gebruikers geen verlopen aanbieding zien.

**Die 24 uur gaat over de prijs die je als *actueel* toont**, niet over wat je zelf hebt gemeten. Je eigen waarnemingen (wat je wanneer bij ons hebt opgehaald) mag je bewaren en tonen zolang je plan loopt, bijvoorbeeld om een opgeblazen referentieprijs te herkennen. Wat niet mag, is die reeks als dataset of feed doorleveren: publiceren als downloadbaar bestand, in een publieke repository, of via een eigen API. Zie ook artikel 6.

Eindigt je plan, je proefperiode of dit contract, dan **verwijder je de via de API verkregen data binnen 14 dagen** uit je systemen, inclusief caches en kopieën. Afgeleide, geaggregeerde gegevens die niet herleidbaar zijn tot onze dataset (bijvoorbeeld een statistiek in een rapport) mag je houden. Op ons verzoek bevestig je de verwijdering schriftelijk.

## 8. Intellectuele eigendom

Productnamen, -beschrijvingen en -afbeeldingen zijn eigendom van de betreffende supermarkten en rechthebbenden; wij claimen daar geen eigendom op. Op de **verzameling** (de genormaliseerde, verrijkte en historische dataset die wij samenstellen en onderhouden) rusten wél onze rechten, waaronder het databankenrecht. Deze voorwaarden geven je gebruiksrecht, geen eigendom.

## 9. Herkomst en betrouwbaarheid van de data

**Waar de data vandaan komt.** Wij verzamelen prijzen en aanbiedingen uit openbare bronnen en uit feeds die ons ter beschikking worden gesteld, één keer per nacht per keten. We loggen nergens in en halen geen gegevens op die achter een account of een betaalmuur staan.

**Wat we vastleggen:** productnaam, merk, prijs, actieprijs en -mechanisme, geldigheidsdatums, EAN, verpakkingsmaat, categorie en de vindplaats van de productafbeelding. **Wat niet:** geen klantgegevens van de supermarkten, en geen voorraad-, marge- of andere bedrijfsgegevens.

**Hoe lang.** Actuele aanbiedingen verdwijnen zodra ze verlopen. Onze eigen waarnemingsreeks (welke prijs wij op welke dag zagen) bewaren we onbeperkt; die reeks is wat Pro en Business ontsluiten.

**Vragen van supermarkten.** Ben je een supermarkt en heb je vragen over hoe wij jouw prijzen verwerken, mail dan [info@prijsprofeet.nl](mailto:info@prijsprofeet.nl).

De data wordt met zorg samengesteld, maar:

- prijzen en aanbiedingen kunnen afwijken van de actuele prijs in de winkel of webshop;
- cross-retailer matches op **EAN** zijn exact, maar niet elke keten publiceert EAN's. Levert een match geen EAN-treffer op, dan volgt een **benadering** op naam, merk en categorie. Die is indicatief en soms onjuist: het is geen productidentiteit;
- dieetclassificaties (bio, vegan, glutenvrij, lactosevrij) worden automatisch afgeleid en zijn indicatief, niet gegarandeerd;
- voorspellingen ("Profeet voorspelt") zijn statistische schattingen, geen toezeggingen.

Bouw je hierop een dienst voor eindgebruikers, dan neem je zelf een passend voorbehoud op en verwijs je gebruikers naar de retailer voor de actuele prijs. De API wordt geleverd **"as is"**, zonder garantie dat de data juist, volledig of geschikt is voor jouw doel.

## 10. Beschikbaarheid, support en wijzigingen

Voor Gratis, Proef en Pro geven we **geen beschikbaarheidsgarantie**. We doen ons best, maar onderhoud, storingen en uitval kunnen voorkomen.

Voor **Business** streven we naar **99,5% beschikbaarheid per kalendermaand** op elke host die je gebruikt (`prijsprofeet.nl`, `prijsprofeet.be`), gemeten met onze eigen monitoring. Elke host wordt apart gemeten; gebruik je er twee, dan geldt de norm voor elk van beide en niet voor een gemiddelde. Halen we de norm op een host die je gebruikt niet, dan krijg je op verzoek een creditering naar rato van de maandprijs. Die creditering is het **enige** middel dat je bij het niet halen van de norm hebt. **Releases en onderhoud tellen gewoon mee**: gaat de API tijdens een update of onderhoud onderuit, dan is dat een storing zoals elke andere. Buiten de meting vallen alleen: **overmacht**, aanvallen op de infrastructuur, storingen bij onze hosting- of CDN-leverancier, en storingen of wijzigingen bij de supermarkten waarvan wij de data betrekken.

**Support** loopt via [info@prijsprofeet.nl](mailto:info@prijsprofeet.nl). We zijn bereikbaar op **werkdagen van 09:00 tot 17:00** (Europe/Amsterdam) en reageren op een storingsmelding die binnen dat venster binnenkomt **binnen één werkdag**. Business-afnemers krijgen daarbij voorrang. Dit is het enige supportkanaal; een melding via een ander kanaal start de termijn niet.

Buiten die uren draait de bewaking gewoon door: een externe probe controleert elke 30 seconden of de API bereikbaar is, alarmen gaan direct naar de beheerder en de diensten herstarten zichzelf na een crash. Dat is **geen 24/7-support**, en we beloven dat ook niet: een storing die op zaterdagavond begint en niet vanzelf herstelt, kan tot de volgende ochtend duren. Live status van website en API, en de maandcijfers uit dit artikel: [status.prijsprofeet.nl](https://status.prijsprofeet.nl) — extern gehost, dus ook te raadplegen tijdens een storing bij ons.

De API is in ontwikkeling: endpoints, velden en dekking veranderen. Bij een **breaking change** op een betaald endpoint informeren we betalende afnemers ten minste **30 dagen** vooraf per e-mail. Niet-brekende wijzigingen (nieuwe velden, nieuwe ketens, betere dekking) voeren we zonder aankondiging door.

## 11. Prijzen, betaling en opzegging

- Prijzen zijn in euro's en **exclusief btw**.
- Betaalde plannen lopen per maand en worden vooraf gefactureerd. Betaaltermijn: 14 dagen.
- Je kunt maandelijks opzeggen tegen het einde van de lopende periode. Reeds betaalde bedragen worden niet terugbetaald.
- Bij niet-betaling mogen we de key opschorten nadat we je een herinnering hebben gestuurd.
- Prijswijzigingen kondigen we minimaal 30 dagen vooraf aan. Ben je het er niet mee eens, dan mag je opzeggen tegen de ingangsdatum.

## 12. Opschorting, beëindiging en het staken van de dienst

We mogen je toegang met onmiddellijke ingang opschorten of beëindigen als je deze voorwaarden schendt (in het bijzonder artikel 6) of als je gebruik de stabiliteit of veiligheid van de dienst in gevaar brengt. Waar dat redelijk is, waarschuwen we eerst. Na beëindiging geldt de verwijderplicht uit artikel 7.

**Stoppen wij zelf met de API**, dan laten we dat betalende afnemers minimaal **3 maanden** vooraf per e-mail weten. Je mag de data die je vóór de einddatum hebt opgehaald in dat geval blijven gebruiken tot het einde van die termijn. Dat is een uitzondering op de verwijderplicht uit artikel 7, zodat je de tijd hebt om over te stappen. Beëindigen we jouw toegang wegens schending van deze voorwaarden, dan geldt die uitzondering niet en blijft artikel 7 onverkort gelden.

## 13. Aansprakelijkheid

Onze aansprakelijkheid is beperkt tot het bedrag dat je in de **12 maanden** voorafgaand aan de schadeveroorzakende gebeurtenis aan ons hebt betaald voor de API. Voor Gratis en Proef betekent dat: onze aansprakelijkheid is uitgesloten, voor zover de wet dat toestaat.

Wij zijn niet aansprakelijk voor indirecte schade, waaronder gederfde winst, gemiste besparingen, omzetverlies, reputatieschade of schade bij jouw klanten, bijvoorbeeld door onjuiste, verouderde of onvolledige prijs-, dieet- of matchingdata, of door onbeschikbaarheid van de API.

Deze beperkingen gelden niet bij opzet of bewuste roekeloosheid van onze kant.

## 14. Zakelijk gebruik

De betaalde plannen (Proef, Pro, Business) worden uitsluitend aangeboden aan **bedrijven en beroepsmatige gebruikers**, niet aan consumenten. Door een key af te nemen bevestig je dat je handelt in de uitoefening van een beroep of bedrijf.

## 15. Persoonsgegevens

De data die de API *teruggeeft* (producten, prijzen, aanbiedingen) bevat **geen persoonsgegevens**. Wie er bij ons binnenkomt, hangt wél af van hoe je bouwt:

- **Server-side** (jouw server bevraagt ons): wij zien alleen jouw server. Er komt geen enkel gegeven van jouw gebruikers bij ons binnen en er is **geen verwerkersovereenkomst** nodig.
- **Device-direct** (de app of browser van jouw gebruiker bevraagt ons rechtstreeks): dan ontvangen wij het IP-adres van die eindgebruiker. Verzoeken met een geldige key **bewaren wij zonder dat IP-adres**: onze toegangslogs laten het veld leeg en houden alleen je partner-id, tijdstip, methode en endpoint over. In onze *fout*logs kan zo'n IP-adres nog voorkomen wanneer een verzoek mislukt (bij een storing of bij weigering wegens overbelasting); ook die bewaren we 30 dagen. Wil je daar aanvullende afspraken over, dan sluiten we op verzoek een verwerkersovereenkomst.

Bouw je server-side, dan is dat ook voor je limiet de betere keuze: met een key telt die op je key in plaats van op één gedeeld IP-adres (artikel 3).

Van afnemers met een key houden we wel gegevens bij: je partnernaam, het **e-mailadres** waarmee je de key hebt aangevraagd (plus de eventuele site of repo die je daarbij opgaf), je plan en limieten, en per verzoek je partner-id, het tijdstip en het endpoint, voor facturatie, limieten, misbruikdetectie en support. We gebruiken dat e-mailadres om je te bereiken over de API zelf: storingen, breaking changes en releasenotes. Geen reclame, en je zit er niet mee in een nieuwsbrief. Toegangslogs bewaren we 30 dagen. Je API-key bewaren we alleen als hash. Zie [Privacy & Cookiebeleid](https://www.prijsprofeet.nl/privacy), artikel 8.

## 16. Wijziging van deze voorwaarden

We kunnen deze voorwaarden wijzigen. Betalende afnemers krijgen wijzigingen minimaal **30 dagen** vooraf per e-mail. Ben je het niet eens met een wijziging, dan kun je opzeggen tegen de ingangsdatum. Voor gebruikers zonder key geldt de versie die op deze pagina staat op het moment van gebruik.

## 17. Toepasselijk recht

Op deze voorwaarden is **Nederlands recht** van toepassing. Geschillen leggen we voor aan de bevoegde rechter in het arrondissement waar Better Call Birdman is gevestigd, tenzij dwingend recht anders bepaalt.

## Contact

Vragen over deze voorwaarden, of over een proefperiode of plan:  
info@prijsprofeet.nl

Better Call Birdman, KvK 84948396
