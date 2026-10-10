<!--
Gegenereerd uit app/templates/seo/api_voorwaarden.html (app-repo, commit 318ffe77)
door scripts/maintenance/export_api_terms.py. Niet met de hand bewerken.
-->

> **Vervallen versie.** Dit is versie 1.0 van de API-voorwaarden, zoals die vanaf 12 juli 2026
> op de site stond. Bindend is de huidige versie op <https://www.prijsprofeet.nl/api-voorwaarden>. Alle versies staan in
> [het overzicht](README.md).

# API-voorwaarden

Versie 1.0 — 12 juli 2026

> **Samenvatting.** Je mag onze data gebruiken om je eigen product te bouwen. Je mag er geen kopie van onze database mee opbouwen, de ruwe data niet doorverkopen, en na afloop van een proefperiode of abonnement verwijder je de opgeslagen data. Prijsdata is indicatief — controleer bij de retailer.

## 1. Wie zijn wij

De PrijsProfeet API wordt aangeboden door **Better Call Birdman**, eenmanszaak, ingeschreven bij de Kamer van Koophandel onder nummer **84948396** ("PrijsProfeet", "wij", "ons"). In deze voorwaarden ben jij ("je", "afnemer") de partij die de API gebruikt.

## 2. Waarop deze voorwaarden van toepassing zijn

Deze voorwaarden gelden voor **alle** toegang tot de API op `prijsprofeet.nl/api/v1/*` — met of zonder API-key, betaald of gratis. Ze gelden niet voor het gewone gebruik van de website; daarvoor geldt onze [disclaimer](https://www.prijsprofeet.nl/disclaimer). Waar deze voorwaarden afwijken van de disclaimer, gaan deze voorwaarden voor als het om de API gaat.

Ons [privacybeleid](https://www.prijsprofeet.nl/privacy) geldt **wél voor allebei**: artikel 8 daarvan beschrijft precies welke gegevens we van API-afnemers verwerken en hoe lang we ze bewaren. Zie ook artikel 14 hieronder.

Je aanvaardt deze voorwaarden:

- **Gratis (zonder key):** door de API te gebruiken. Er is geen registratie, dus gebruik geldt als aanvaarding.
- **Proef, Pro en Business:** door de API-key in gebruik te nemen. We sturen deze voorwaarden mee met de e-mail waarin je de key ontvangt, vóórdat er een factuur volgt.

## 3. De plannen

| Plan | Toegang | Limiet | Commercieel gebruik | Bronvermelding | SLA |
|---|---|---|---|---|---|
| **Gratis** | Publieke endpoints, geen key nodig | 60 req/min | Ja | Verplicht | Nee |
| **Proef** | Alles uit Pro, tijdelijk | 300 req/min | Nee — alleen evaluatie | Verplicht | Nee |
| **Pro** | + `/match/*` en `/price-history` | 300 req/min | Ja | Niet nodig | Nee |
| **Business** | Alles uit Pro | tot 1.000 req/min | Ja | Niet nodig | Ja, zie artikel 9 |

Actuele prijzen staan op de [API-pagina](https://www.prijsprofeet.nl/api). Prijzen zijn exclusief btw.

## 4. Proefperiode

Op verzoek geven we een **proefperiode van 14 dagen** met Pro-functionaliteit, gratis en zonder betaalgegevens. Daarvoor gelden een paar extra regels:

- De proef is bedoeld om te **evalueren**, niet om er een product mee in productie te draaien of om er commercieel voordeel uit te halen.
- De proef loopt **automatisch af**. De key stopt op de einddatum met werken; wij hoeven niets op te zeggen en jij ook niet.
- Eén proefperiode per organisatie. Een proef gaat alleen over in een betaald plan als je daar expliciet mee instemt — er wordt niets automatisch omgezet of afgeschreven.
- Tijdens de proef gelden geen beschikbaarheidsgaranties en is onze aansprakelijkheid uitgesloten voor zover de wet dat toestaat.

> **Verwijderplicht na afloop.** Binnen **14 dagen** na het einde van de proefperiode verwijder je alle via de API verkregen data uit je systemen — inclusief caches, kopieën, exports en back-ups voor zover technisch mogelijk. Je mag de data uit een proef dus niet houden of blijven gebruiken nadat de proef is afgelopen. Op ons verzoek bevestig je de verwijdering schriftelijk. Deze plicht geldt ook na beëindiging van een betaald plan (artikel 6).

## 5. Wat je met de data mag — en niet mag

Zolang je plan loopt, geven we je een **niet-exclusief, niet-overdraagbaar en herroepbaar** recht om de data via de API op te vragen en te verwerken in je eigen product, dienst, onderzoek of interne tool.

Niet toegestaan is:

- **De dataset nabouwen.** Systematisch of grootschalig data onttrekken om (een substantieel deel van) onze database te reconstrueren, na te bouwen of te dupliceren.
- **Doorverkoop van ruwe data.** De data as-is doorverkopen, doorleveren of als eigen datafeed of API aanbieden. Een product bouwen dát op de data draait mag wel — de data zelf doorverkopen niet.
- **Limieten omzeilen.** Meerdere keys of accounts gebruiken, keys delen met derden, of langs de rate limits werken.
- **Suggereren dat een supermarkt erachter zit.** Wij zijn onafhankelijk en hebben geen band met de genoemde ketens; presenteer de data niet als afkomstig van of goedgekeurd door een retailer.
- Gebruik dat in strijd is met de wet of dat de dienst, de infrastructuur of andere gebruikers schaadt.

**Bronvermelding — alleen voor Gratis en Proef.** Gebruik je de API zonder key of tijdens een proefperiode, en zien jouw gebruikers de data, dan vermeld je zichtbaar **PrijsProfeet** als bron met een link naar `prijsprofeet.nl`, op elk scherm of elke pagina waar die data staat. Wie niets betaalt, betaalt in bronvermelding.

**Pro en Business zijn hiervan vrijgesteld** — je mag de data zonder bronvermelding in je eigen product verwerken.

## 6. Caching, opslag en verwijdering

Je mag data cachen en opslaan zolang je plan loopt — dat hoort bij normaal gebruik. Prijzen veranderen wekelijks: cache prijsdata niet langer dan 24 uur, zodat je gebruikers geen verlopen aanbieding zien.

Eindigt je plan, je proefperiode of dit contract, dan **verwijder je de via de API verkregen data binnen 14 dagen** uit je systemen, inclusief caches en kopieën. Afgeleide, geaggregeerde gegevens die niet herleidbaar zijn tot onze dataset (bijvoorbeeld een statistiek in een rapport) mag je houden. Op ons verzoek bevestig je de verwijdering schriftelijk.

## 7. Intellectuele eigendom

Productnamen, -beschrijvingen en -afbeeldingen zijn eigendom van de betreffende supermarkten en rechthebbenden; wij claimen daar geen eigendom op. Op de **verzameling** — de genormaliseerde, verrijkte en historische dataset die wij samenstellen en onderhouden — rusten wél onze rechten, waaronder het databankenrecht. Deze voorwaarden geven je gebruiksrecht, geen eigendom.

## 8. De data is indicatief

Wij verzamelen prijzen uit openbare bronnen van tien supermarkten. De data wordt met zorg samengesteld, maar:

- prijzen en aanbiedingen kunnen afwijken van de actuele prijs in de winkel of webshop;
- cross-retailer matches op **EAN** zijn exact, maar niet elke keten publiceert EAN's. Levert een match geen EAN-treffer op, dan volgt een **benadering** op naam, merk en categorie. Die is indicatief en soms onjuist — het is geen productidentiteit;
- dieetclassificaties (bio, vegan, glutenvrij, lactosevrij) worden automatisch afgeleid en zijn indicatief, niet gegarandeerd;
- voorspellingen ("Profeet voorspelt") zijn statistische schattingen, geen toezeggingen.

Bouw je hierop een dienst voor eindgebruikers, dan neem je zelf een passend voorbehoud op en verwijs je gebruikers naar de retailer voor de actuele prijs. De API wordt geleverd **"as is"**, zonder garantie dat de data juist, volledig of geschikt is voor jouw doel.

## 9. Beschikbaarheid, SLA en wijzigingen

Voor Gratis, Proef en Pro geven we **geen beschikbaarheidsgarantie**. We doen ons best, maar onderhoud, storingen en uitval kunnen voorkomen.

Voor **Business** streven we naar **99,5% beschikbaarheid per kalendermaand**, gemeten met onze eigen monitoring. Halen we dat niet, dan krijg je op verzoek een creditering naar rato van de maandprijs. Die creditering is het **enige** middel dat je bij het niet halen van de norm hebt. Buiten de meting vallen: **onderhoud en releases** — we brengen regelmatig updates uit en elke release herstart de dienst kortstondig — **overmacht**, aanvallen op de infrastructuur, storingen bij onze hosting- of CDN-leverancier, en storingen of wijzigingen bij de supermarkten waarvan wij de data betrekken.

De API is in ontwikkeling: endpoints, velden en dekking veranderen. Bij een **breaking change** op een betaald endpoint informeren we betalende afnemers ten minste **30 dagen** vooraf per e-mail. Niet-brekende wijzigingen (nieuwe velden, nieuwe ketens, betere dekking) voeren we zonder aankondiging door.

## 10. Prijzen, betaling en opzegging

- Prijzen zijn in euro's en **exclusief btw**.
- Betaalde plannen lopen per maand en worden vooraf gefactureerd. Betaaltermijn: 14 dagen.
- Je kunt maandelijks opzeggen tegen het einde van de lopende periode. Reeds betaalde bedragen worden niet terugbetaald.
- Bij niet-betaling mogen we de key opschorten nadat we je een herinnering hebben gestuurd.
- Prijswijzigingen kondigen we minimaal 30 dagen vooraf aan. Ben je het er niet mee eens, dan mag je opzeggen tegen de ingangsdatum.

## 11. Opschorting en beëindiging

We mogen je toegang met onmiddellijke ingang opschorten of beëindigen als je deze voorwaarden schendt — in het bijzonder artikel 5 — of als je gebruik de stabiliteit of veiligheid van de dienst in gevaar brengt. Waar dat redelijk is, waarschuwen we eerst. Na beëindiging geldt de verwijderplicht uit artikel 6.

## 12. Aansprakelijkheid

Onze aansprakelijkheid is beperkt tot het bedrag dat je in de **12 maanden** voorafgaand aan de schadeveroorzakende gebeurtenis aan ons hebt betaald voor de API. Voor Gratis en Proef betekent dat: onze aansprakelijkheid is uitgesloten, voor zover de wet dat toestaat.

Wij zijn niet aansprakelijk voor indirecte schade, waaronder gederfde winst, gemiste besparingen, omzetverlies, reputatieschade of schade bij jouw klanten — bijvoorbeeld door onjuiste, verouderde of onvolledige prijs-, dieet- of matchingdata, of door onbeschikbaarheid van de API.

Deze beperkingen gelden niet bij opzet of bewuste roekeloosheid van onze kant.

## 13. Zakelijk gebruik

De betaalde plannen (Proef, Pro, Business) worden uitsluitend aangeboden aan **bedrijven en beroepsmatige gebruikers**, niet aan consumenten. Door een key af te nemen bevestig je dat je handelt in de uitoefening van een beroep of bedrijf.

## 14. Persoonsgegevens

De data die de API teruggeeft — producten, prijzen, aanbiedingen — bevat **geen persoonsgegevens**. Er is dus geen verwerkersovereenkomst nodig.

Van afnemers met een key houden we wel gegevens bij: je partnernaam, je contactgegevens uit onze correspondentie, je plan en limieten, en per verzoek je partner-id, het tijdstip en het endpoint — voor facturatie, limieten, misbruikdetectie en support. Toegangslogs bewaren we 30 dagen. Je API-key bewaren we alleen als hash. Zie [Privacy & Cookiebeleid](https://www.prijsprofeet.nl/privacy), artikel 8.

## 15. Wijziging van deze voorwaarden

We kunnen deze voorwaarden wijzigen. Betalende afnemers krijgen wijzigingen minimaal **30 dagen** vooraf per e-mail. Ben je het niet eens met een wijziging, dan kun je opzeggen tegen de ingangsdatum. Voor gebruikers zonder key geldt de versie die op deze pagina staat op het moment van gebruik.

## 16. Toepasselijk recht

Op deze voorwaarden is **Nederlands recht** van toepassing. Geschillen leggen we voor aan de bevoegde rechter in het arrondissement waar Better Call Birdman is gevestigd, tenzij dwingend recht anders bepaalt.

## Contact

Vragen over deze voorwaarden, of over een proefperiode of plan:  
info@prijsprofeet.nl

Better Call Birdman — KvK 84948396
