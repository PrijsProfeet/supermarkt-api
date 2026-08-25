# Changelog

Wijzigingen aan de publieke API van [PrijsProfeet](https://www.prijsprofeet.nl/api).
De meest recente staan ook op [/api](https://www.prijsprofeet.nl/api#wat-is-nieuw);
dit is het volledige archief.

Elke wijziging krijgt hier een **GitHub Release**. Zet de repo op *Watch → Releases*
als je bericht wilt krijgen zonder een pagina in de gaten te houden.

Nieuwe velden, nieuwe ketens en betere dekking rollen we zonder aankondiging uit.
**Breaking changes op een betaald endpoint kondigen we minimaal 30 dagen van tevoren
aan** (art. 10 van de [API-voorwaarden](https://www.prijsprofeet.nl/api-voorwaarden)):
per e-mail aan betalende afnemers én hier.

## 2026-08-25

**Zoekresultaten staan in een andere volgorde — zelfde velden, zelfde aantal.** Onze
relevantie-sortering woog mee hoe lang een productnaam is, en dat is een huisconventie
van de keten en geen eigenschap van de aanbieding. Ketens die hun producten uitgebreid
benoemen zakten daardoor structureel naar onderen: op `Doritos` stonden de drie
Jumbo-rijen op plek 30 t/m 32 van 33. **Naamlengte telt niet meer mee**; bij gelijke
relevantie beslist de prijs, oplopend. **Geen schemawijziging** — maar sorteer je zelf
niet na, dan krijg je een andere volgorde terug dan voorheen.

**Nieuw op `/search`: de parameter `include_all_retailers` en het veld
`retailer_preference`.** Allebei alleen van betekenis voor browserverkeer met een
`pp_uid`-cookie, waar een opgeslagen winkelvoorkeur de resultaten versmalt. **Voor
integraties met een API-sleutel verandert er niets**: er is geen voorkeur om toe te
passen, dus de parameter doet niets en het veld is altijd `null`. Puur toegevoegd.

**`openapi.json` bevat geen interne modellen meer: 59 schema's → 12.** De spec filterde
de interne endpoints wel uit de `paths`, maar niet uit `components.schemas` — die worden
uit de routes verzameld vóórdat dat filter draait. Daardoor stonden 47 modellen in de
spec die vanaf geen enkel gedocumenteerd endpoint bereikbaar waren, zoals
`UserDataExport`, `PushSubscription` en `ScraperMetrics`. **Geen enkel endpoint en geen
enkel gedocumenteerd model is verdwenen** — alle 24 paden staan er nog. Genereer je een
client uit deze spec, dan krijg je voortaan alleen klassen die je ook echt kunt
gebruiken.

## 2026-08-09

**De OpenAPI-specificatie is nu machinaal op te halen.** Tot nu toe was de spec alleen
in een browser te bekijken op [/docs](https://www.prijsprofeet.nl/docs);
geautomatiseerde clients krijgen daar een `403`, dus codegeneratie was onmogelijk.
[`openapi.json`](openapi.json) in deze repo is de kopie die je wél kunt ophalen. Geen
wijziging aan de API zelf.

## 2026-08-01

**Nieuw: `retailer_category` — de categorie zoals de keten hem zélf publiceert.** Staat op `/products` en `/products/{id}`. `unified_category` is onze normalisatie over 10 ketens; dit is de onbewerkte schapindeling van de winkel erachter, letterlijk overgenomen. **Puur toegevoegd** — geen bestaand veld gewijzigd of verwijderd.

**Let op: die strings zijn niet vergelijkbaar tússen ketens.** Elke keten heeft zijn eigen taxonomie ("Aardappelen, groente en fruit" bij Jumbo, "Aardappelen, groente, fruit" bij PLUS, "AGF" bij Ekoplaza). Wil je één noemer over alle ketens, blijf dan bij `unified_category`.

**Dekking, gemeten op 1 aug over 10.450 lopende en aankomende acties: 87,7%.** PLUS, DekaMarkt, Dirk en Ekoplaza 100%, Jumbo 99,9%, Albert Heijn 97,9% (die publiceert `Hoofdcategorie/Subcategorie`, 676 verschillende waarden). **Aldi, Hoogvliet en Vomar publiceren géén categorie** — daar is het veld `null`. **En Lidl publiceert op élk product dezelfde waarde `"Food"`**: het veld is er wel, maar zegt niets. Val je terug op `unified_category`, controleer dan niet alleen op `null` maar behandel `"Food"` als afwezig.

Niet op `/search`: die respons is ongewijzigd. Gevraagd door een afnemer die per keten synchroniseert — blijf zulke verzoeken vooral sturen.

## 2026-07-28

**DekaMarkt: procentkortingen stonden op de schapprijs, en acties liepen een dag te lang.** Twee correcties die je data merkbaar veranderen. **Geen schemawijziging** — zelfde velden, zelfde volgorde, alleen betere waarden.

**1. Een "25% KORTING"-actie stond op de volle prijs.** De bron geeft bij zo'n actie dezelfde prijs terug als actieprijs én als normale prijs, dus zagen wij geen korting: het product kwam binnen op de schapprijs, zónder doorstreepprijs. Dat raakte 107 van de 112 procentacties — een smoothie met 50% korting stond op €2,75 in plaats van €1,38. **Prijzen bij DekaMarkt kunnen dus flink lager zijn dan wat je gisteren ophaalde, en `original_price` is nu gevuld waar je eerder `null` kreeg.** `unit_price` rekent mee.

**2. `valid_until` liep één dag te ver door.** DekaMarkt geeft als einddatum de *wisseldag* terug, niet de laatste geldige dag; Dirk geeft wél de laatste geldige dag, en dat verschil liep door dezelfde regel code. Een DekaMarkt-actie eindigt nu een dag eerder dan je gewend was. Filter je op `valid_until`, dan verdwijnen verlopen acties nu op het juiste moment — en verschijnt dezelfde actie niet meer twee keer op de wisseldag, tegen twee prijzen.

Beide correcties zijn met terugwerkende kracht doorgevoerd in het prijsverloop (`/price-history`): 2.231 rijen. Cachet je onze data, ververs dan je DekaMarkt-rijen. Andere ketens zijn niet geraakt.

## 2026-07-23

**`/deals/top` geeft nu `valid_from` en `valid_until` terug.** Die twee velden zaten er niet in — niet leeg, maar volledig afwezig — dus je kon niet zien wanneer een aanbieding afloopt. Cachet je onze respons en ververs je op je eigen schema, dan is dat een probleem: actieweken rollen *midweeks* om, dus een deal kan tussen twee verversingen verlopen en dan toon je de prijs van vorige week. Beide velden staan nu in `representative_product`; controleer `valid_until` voor je rendert. **Puur toegevoegd** — bestaande velden en volgorde zijn ongewijzigd, dus je integratie blijft werken. Gemeld door een gebruiker wiens dashboard hier tegenaan liep; blijf zulke dingen vooral sturen.

## 2026-07-14

**Nieuw: `?current_only=true` op `/match/*`.** Wil je alleen matches die je vandáág kunt kopen, zet 'm aan — dan vallen acties van volgende week en recent gerekende prijzen eruit. **Let op dat dit dekking kost:** op onze eigen vergelijkkaarten houdt 29% van de producten dan géén enkele match over. Daarom staat hij standaard uit.

**De standaardvolgorde verandert niet.** We overwogen de geldige matches vooraan te zetten, zodat een simpele `matches[0]` altijd klopt — maar we hebben *"gesorteerd op prijs"* gedocumenteerd, en artikel 10 van de voorwaarden verplicht ons betalende afnemers 30 dagen vooraf te informeren bij een breaking change op een betaald endpoint. Een parameter erbij mag meteen; de volgorde omgooien niet. Wil je die wijziging, laat het weten — dan kondigen we 'm netjes aan.

## 2026-07-14

**De goedkoopste match is niet altijd te koop — nu staat het er ook bij.** `/match/*` gaf altijd al acties terug die pas *volgende week* beginnen (ongeveer een kwart van de catalogus) en rijen met de prijs die een keten *recent* rekende. Dat is opzet: "volgende week bij Jumbo goedkoper" is precies wat je gebruiker wil weten. Maar ons voorbeeld liet die velden niet zien, en een `min(price)` over alle matches geeft dus een prijs die vandaag niet bestaat. **De respons is niet veranderd** — `is_current_deal`, `promotion_status` en `valid_from` zaten er al in; ze staan nu in het voorbeeld en in de docs. Filter of label erop.

Ook gecorrigeerd: bij zes multipacks stond de verpakkingsgrootte van *één stuk* in `quantity`, waardoor `unit_price` onzin was (een sixpack Dr Pepper stond op €2.090,91 per liter). Parseer je `unit_price`, dan kunnen die waarden dus gewijzigd zijn — in je voordeel.

## 2026-07-14

**De benadering op `/match/*` is scherper — en geeft nu `quantity` terug.** Twee dingen die voor je integratie uitmaken.

**1. `quantity` was altijd `null` op een benaderde match.** Het veld zat wél in de index, maar we vroegen het nooit op. Vanaf nu staat de verpakkingsgrootte er gewoon in (`"6 x 0,33 l"`, `"330 ml"`). Parse je die: hij kan nu dus gevuld zijn waar je eerder altijd `null` kreeg.

**2. Een sixpack wordt niet meer naast een los blikje gezet.** De maat-controle keek naar de productnaam, en die noemt maar bij ~16% van de producten een formaat — bij *"Grolsch Premium pilsner blik tray"* staat het nergens. Daardoor kon een 6-pack naast een enkel blikje van een ander merk van €0,67 belanden: op een prijsvergelijker leest dat als "6× goedkoper elders". We kijken nu naar het `quantity`-veld (dat bij ~79% van de producten gevuld is), en een ander merk komt niet meer náást het echte merk te staan. Gemeten over 1.500 gevallen: **577 foute regels minder, en precies één goede regel verloren**. Een benadering blijft een benadering — indicatief, geen productidentiteit.

## 2026-07-14

**Gratis key, direct te krijgen — en hij telt op je key.** Vraag er [hier](https://www.prijsprofeet.nl/api#gratis-key) een aan: mail je adres, klik de link, key op je scherm. Geen wachttijd en geen verkoopgesprek. Je limiet wordt **150/min op je key** in plaats van 30–120/min per endpoint op je IP — vooral op de lijst- en bulk-endpoints (30/min) scheelt dat een factor 5. De blokkade op `bot`/`crawler` in je User-Agent geldt met een key ook niet meer. Zonder key blijft alles werken zoals het werkte; er komt geen slot op.

## 2026-07-14

**Ekoplaza-dekking van 24% naar 95%.** Ekoplaza's EAN's stonden al in de bron, maar we haalden ze maar bij een vijfde van de aanbiedingen op. Nu bij vrijwel alle. Let op: Ekoplaza is volledig biologisch en deelt zijn EAN's met géén andere keten, dus dit levert wél product-identiteit op `/products/*` en `/match/ean/{ean}`, maar géén nieuwe cross-retailer matches. Producten zonder EAN zijn weeg-artikelen uit de winkel (los fruit, kaas van het mes) — dat zijn geen GTIN's en die geven we bewust niet als EAN terug.

## 2026-07-13

**PLUS levert nu EAN's — en komt in de exacte matching.** Dekking van 0% naar **100%**, en PLUS deelt nu **1.165 EAN's** met Albert Heijn, Jumbo, Dirk en DekaMarkt. Daarmee is PLUS in één klap de grootste bron van exacte cross-retailer matches via `/match/*`. Ook het aanbod groeide fors: van ~275 naar ~2.100 producten.

## 2026-07-12

**Pro en Business tellen nu op je key, niet op je IP.** Bouw je server-side, dan deelde je hele gebruikersbestand één IP-limiet. Betaalde plannen krijgen hun eigen budget (300 resp. 1.000/min) los van het IP. De gratis limieten staan per endpoint (30–120/min per IP) — eerder noemden we hier één getal dat niet klopte.

## 2026-07-12

**`/deals/top` filtert nu op retailer.** Geef één of meer ketens mee (`?retailer=albert_heijn&retailer=jumbo`) om de toplijsten te beperken tot de winkels die jij bedient. Eerder stond hier een `/deals`-endpoint vermeld dat niet bestond — dat is gecorrigeerd.

## 2026-07-11

**DekaMarkt levert nu EAN's.** Dekking van 0% naar 98% — exacte cross-retailer matching via `/match/*` loopt nu ook langs DekaMarkt.

## 2026-07-10

**Dirk levert nu EAN's.** Dekking van 0% naar 99% — exacte cross-retailer matching via `/match/*` loopt nu ook langs Dirk.

## 2026-07-10

**Gratis tier heeft geen key meer nodig.** Zoeken, producten en aanbiedingen zijn direct te gebruiken, zonder registratie. *Het getal dat hier eerst stond (60/min) klopte niet en is verwijderd; de limieten die nu gelden staan [op de API-pagina](https://www.prijsprofeet.nl/api#rate-limits).*

## 2026-06-20

**Benadering als terugval op `/match/*`.** Levert een product geen EAN-match op, dan volgt een benadering op naam, merk en categorie (indicatief, geen productidentiteit).

## 2026-06-17

**Jumbo EAN-dekking hersteld naar 99%.** Meer betrouwbare cross-retailer matches tussen Albert Heijn en Jumbo.
