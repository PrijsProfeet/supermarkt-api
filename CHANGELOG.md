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

## 2026-09-08

**Nieuw in `openapi.json`: de API-sleutel staat er nu in als security scheme
(`ApiKeyAuth`, header `X-API-Key`).** Op `/docs` krijg je daardoor een
*Authorize*-knop: je voert je sleutel eenmalig in en hij gaat automatisch mee.
Genereer je een client uit de spec, dan kent die de header nu ook — tot nu toe
stond hij alleen in het proza op `/api`, dus een gegenereerde client wist niet
dat hij bestond. Gemeld door een afnemer die elke beveiligde route met een
handgebouwde `curl` moest proberen.

**Waar hij verplicht is en waar niet.** Op `/match/*` en
`/products/{id}/price-history` staat de sleutel als vereist; dat zijn de twee
endpoints die een betaald plan vragen. Op de gratis endpoints (`/search`,
`/products`, `/deals`, `/categories`, `/filter-stats`) staat hij als optioneel —
die werken zonder sleutel en dat blijft zo. Meesturen loont daar wel: met
sleutel val je onder het ratelimiet van je plan in plaats van onder de anonieme
limiet per endpoint, die op `/products` 30 per minuut is.

**Gecorrigeerd: `/products/{id}` gaf een `404` op `base_product_id`.** Dat is
precies het veld waarvan we [op 6 september](#2026-09-06) schreven dat je erop
moet dedupliceren — en het was het enige id dat de route niet kon beantwoorden.
Oorzaak: het stabiele id staat op geen enkele rij opgeslagen, we leiden het af
bij het uitlezen, en de route zocht exact. Gemeten over 200 producten per keten:
**1.393 van de 1.393** stabiele ids gaven een `404`, bij alle zeven ketens die
een weekdatum in het `product_id` dragen (Albert Heijn, Aldi, Lidl, PLUS, Dirk,
DekaMarkt, Hoogvliet). Bij Jumbo, Ekoplaza en Vomar zit er geen datum in het id,
dus daar speelde het niet.

**Puur verruimend.** Een gedateerd `product_id` werkt onveranderd; wat eerst een
`404` gaf, geeft nu de actie die op dat moment loopt. Hetzelfde gold voor
`/match/product/{product_id}`, ook opgelost.

**Verduidelijkt: `/match/ean/{ean}` waarschuwt nu dat een GTIN geen
verpakkingsmaat is.** Het endpoint is bewust ongegate — het moet alles met die
barcode teruggeven — maar de beschrijving zei alleen "for price comparison", en
dat nodigt uit tot een `min(price)` over rijen die verschillende verpakkingen
zijn. Eén EAN kan het blik, de multipack en de tray zijn: `5000112658620` draagt
bij Albert Heijn een blik van EUR 0,85, een 8-pack van EUR 5,19 en een 20-pack
van EUR 13,19. Filter op `quantity`, dat op elke match staat, of gebruik
`/match/product/{product_id}`, dat die controle voor je doet. Alleen de tekst in
de spec wijzigde; het gedrag niet.

**Genereer je client opnieuw** als je hem uit de spec bouwt: `openapi.json`
draagt een nieuw `components.securitySchemes` en een `security`-blok per
operatie. Er is geen veld bijgekomen of verdwenen, en er is geen pad bijgekomen
of verdwenen.

## 2026-09-06

**Nieuw op elke route die een product teruggeeft — `/products`,
`/products/{id}`, `/products/promotional/all`, `/products/search/{q}`,
`/products/folder/{id}` en `/products/retailer/{r}`: `base_product_id` — het
`product_id` zonder de weekdatum, en dus de sleutel om op te dedupliceren.** Een `product_id` draagt de actieweek, dus dezelfde SKU krijgt
een nieuw id zodra er een actie begint. Wie op `product_id` ontdubbelt ziet een
heraangeboden artikel daardoor als een nieuw product. Gemeld door een afnemer die
vier Aldi-artikelen elke nacht opnieuw binnenkreeg: Aldi vernieuwt die dagelijks,
zelfde artikel, zelfde prijs, venster één dag opgeschoven — `1233345_2026-09-05`
en `1233345_2026-09-06` zijn allebei `base_product_id: "1233345"`.

**Het veld bestond al op `/search`; het ontbrak op precies de routes die je
paginert.** Dat was een omissie, geen keuze — we berekenen die sleutel al bij het
indexeren.

**Puur toegevoegd, en altijd gevuld.** Bestaande velden veranderen niet. Bij
Jumbo, Ekoplaza en Vomar staat er geen datum in het `product_id`, dus daar is het
gelijk aan `product_id` — nooit leeg, zodat je er niet per keten een uitzondering
voor hoeft te maken. **Let op bij Vomar:** die ids worden per folder afgeleid en
rotéren wekelijks, dus daar dedupliceert het veld niet over weken heen. Het is
geen sleutel tussen ketens; gebruik daarvoor `ean`.

Het veld staat nieuw in `openapi.json` op `ProductResponse`.

## 2026-09-04 (4)

**Gecorrigeerd: `min_valid_from` en `max_valid_from` werkten alleen op
`/products`, niet op `/products/promotional/all`.** Op die tweede route kreeg je
een `200` met het volle totaal, ongeacht de datum — een onbekende parameter wordt
stil genegeerd, en dat leest als een antwoord. Gemeld door een afnemer, een dag
na de introductie. Beide routes lezen nu hetzelfde filter, met dezelfde `422` op
een datum die we niet kunnen lezen. De twee parameters staan nieuw in
`openapi.json` voor die route.

**Nieuw op `/match/*`: `price_changed_at` op een `shelf`-rij — sinds wanneer die
reguliere prijs geldt.** Een tijdstip in ISO 8601 met Nederlandse offset
(`2026-09-04T01:38:22+02:00`). Spiegel je schapprijzen, dan kun je een rij
overslaan waarvan de prijs sinds je vorige ophaal niet bewoog, in plaats van hem
opnieuw te verwerken. Op `active`-, `upcoming`- en `historical`-rijen is het veld
`null`: een actie heeft een venster (`valid_from`/`valid_until`), geen "sinds".

**Puur toegevoegd.** Bestaande velden veranderen niet. Het veld staat in
[`examples/matching.py`](examples/matching.py); de respons van `/match/*` is in
de spec een ongetypeerd object, dus voor dat deel hoeft geen client opnieuw.

## 2026-09-04 (3)

**De API-voorwaarden zijn op twee punten verduidelijkt, allebei in jouw voordeel.**
Versie 1.2 (31 augustus, artikel 7) en versie 1.3 (3 september, artikel 6). Er
verdwijnt geen recht en er komt geen verbod bij: de tekst zegt nu wat hij al
bedoelde. We kondigen het aan omdat een verduidelijking die je niet leest niets
verduidelijkt — verplicht is het niet, want artikel 16 vraagt een termijn van 30
dagen bij een wijziging en dit versmalt niets.

**Artikel 7 — je eigen waarnemingen mag je bewaren.** De regel "cache prijsdata niet
langer dan 24 uur" maakte geen onderscheid en las dus als een verbod op onthouden wat
je zelf gemeten hebt. Die 24 uur gaat over de prijs die je als **actueel** toont. Wat
je wanneer bij ons hebt opgehaald mag je bewaren en tonen zolang je plan loopt —
bijvoorbeeld om een opgeblazen referentieprijs te herkennen. Wat niet mag, is die
reeks doorleveren als dataset of feed: publiceren als downloadbaar bestand, in een
publieke repository, of via een eigen API.

**Artikel 6 — de grens bij "nabouwen" gaat over hoe je ophaalt, niet over hoeveel je
bewaart.** Het verbod stond geformuleerd als een intentie ("data onttrekken *om* onze
database te reconstrueren") en dat kan niemand toetsen — wij niet over jou, en
belangrijker: jij niet over jezelf. Wie zich aan de regel wil houden moet kunnen
nagaan of hij dat doet. De waarneembare toets staat er nu naast:

- Vraag je op wat je gebruikers of je product nodig hebben, dan is dat **normaal
  gebruik** — ook als er na een jaar veel ligt, en ook als het schapprijzen zijn en
  niet alleen aanbiedingen.
- Loop je onze catalogus af om hem te vullen (alle producten of alle EAN's op rij,
  ongeacht of iemand ernaar vroeg), dan is dat **onttrekken**, ook als het er weinig
  zijn.

**Waarom nu.** Twee afnemers stelden hier in vier dagen tijd dezelfde vraag over —
mag ik houden wat ik zelf heb opgehaald — en kregen het antwoord geen van beiden uit
de tekst. Als twee mensen die de voorwaarden hebben gelézen het er niet uit halen,
dan ligt dat aan de tekst. Dezelfde vraag staat nu ook in de FAQ op
[/api](https://www.prijsprofeet.nl/api), want alleen de juridische tekst aanpassen
herhaalt precies die fout.

**Niets te doen.** Geen schemawijziging, geen veld erbij of eraf, `openapi.json`
ongewijzigd. Je hoeft geen client opnieuw te genereren.

## 2026-09-04 (2)

**Nieuw op `/search`: `unmatched_terms` — de woorden uit je zoekopdracht die
niets opleveren.** Zoek je op twee woorden waarvan er één nergens op slaat, dan
gaf het antwoord tot nu toe gewoon resultaten voor de rest, zonder enig signaal.
Gemeten: `zzzzz barista` gaf **exact hetzelfde antwoord** als `oatly barista`, en
`oatly chips` gaf 84 producten die allemaal Lay's waren — terwijl er geen enkel
Oatly-product in de catalogus stond.

**Puur toegevoegd.** `results`, `total` en de rest veranderen niet; laat je het
veld links liggen, dan blijft alles zoals het was. Wel nieuw in `openapi.json`,
dus **genereer je client opnieuw** als je die uit de spec bouwt.

**Wat je ermee kunt.** Is `unmatched_terms` niet leeg, dan beantwoorden de
resultaten alleen de rest van de zoekopdracht. Dat is precies het geval waarin je
gebruiker denkt dat wij een merk voeren dat wij niet voeren. Wij zetten er zelf
"Geen resultaten voor *oatly*. Hieronder alles voor *barista*." boven.

**Wanneer het gevuld is.** Alleen bij zoekopdrachten van twee of meer woorden die
op de fuzzy terugval uitkomen. Een exact resultaat vereist de héle zoekopdracht,
dus daar kan per definitie geen woord zijn weggevallen — het veld is dan leeg. Een
woord dat alléén fuzzy matcht telt als gevonden; dat heeft wél bijgedragen. En
slaan álle woorden nergens op terwijl er toch resultaten zijn, dan blijft het veld
leeg: een melding die de hele zoekopdracht ontkent terwijl er resultaten staan is
misleidender dan geen melding.

## 2026-09-04

**Dirk en DekaMarkt leveren nu ook schapprijzen — `promotion_status: "shelf"`
komt bij drie ketens vandaan in plaats van bij één.** Tot nu toe kwam die vierde
status alleen van PLUS. Een match waarin Dirk of DekaMarkt deze week niets
promoot, draagt voortaan hun reguliere prijs van vandaag in plaats van de laatste
prijs die wij daar toevallig zagen — of in plaats van helemaal niets.

**Geen schemawijziging.** Zelfde velden, zelfde vorm; alleen meer en betere rijen
in `/api/v1/match/*`. Wat je merkt:

- **Meer ketens per match.** Gemeten over onze eigen live catalogus komen er
  1.713 rijen bij op producten waar die keten vandaag níet in het antwoord staat,
  en 231 producten worden voor het eerst überhaupt vergelijkbaar.
- **Verse in plaats van oude prijzen.** 2.843 rijen die nu `historical` zijn
  (maximaal 60 dagen oud) worden `shelf`. ⚠️ Als je op die status filtert of erop
  labelt: dezelfde SKU kan dus van `historical` naar `shelf` verspringen zonder
  dat de prijs verandert — 92,8% van die rijen draagt exact hetzelfde bedrag.
- **Verpakkingsmaat gevuld.** De schaprijen dragen `quantity` en, waar die
  parseerbaar is, `unit_price`/`unit`. Een prijs zonder de verpakking is niet
  vergelijkbaar.

**Wat het niet is:** een volledig assortiment per keten in de API. De schaprijen
voeden de matching; ze verschijnen niet als losse producten in `/products` of
`/search` (een schapprijs is geen aanbieding).

## 2026-09-03 (2)

**Nieuw op `/search`: `brand_hub` — de merkpagina die bij deze zoekopdracht
hoort.** Zoek je op een merk (`?q=oatly`, maar ook `?q=oatly%20barista`), dan
draagt het antwoord voortaan een extra veld met de merkpagina erbij: naam, slug,
url, bij hoeveel ketens dat merk in de actie is geweest en over hoeveel
promoweken. Is de zoekopdracht geen merk, dan is het veld `null`.

**`results` verandert niet.** Het veld staat er náást, niet in — precies zodat
een integratie die de productlijst uitleest hier niets van merkt. Puur
toegevoegd; laat je het veld links liggen, dan blijft alles zoals het was.

Gematcht op de langste prefix van de zoekopdracht, hoofdletter- en
leestekenongevoelig: `Hertog Jan krat` komt bij het bier uit en niet bij het
gelijknamige ijs.

## 2026-09-03

**Nieuw op `/products`: filteren op de startdag van een actie — `min_valid_from`
en `max_valid_from`.** Allebei optioneel, allebei inclusief, in de vorm
`YYYY-MM-DD` (bijvoorbeeld `?min_valid_from=2026-09-03`). Gevraagd door een
afnemer die wekelijks synchroniseert en tot nu toe de hele lijst moest ophalen om
er een paar honderd nieuwe acties uit te vissen. **Puur toegevoegd** — laat je ze
weg, dan verandert er niets aan het antwoord.

**Een datum die we niet kunnen lezen geeft een `422`, geen genegeerde parameter.**
`valid_from` is een datumstring, dus de vergelijking is lexicografisch:
`2026-9-1` of `01-09-2026` zou een `200` opleveren met de verkeerde rijen. Het
antwoord noemt de parameter en de verwachte vorm. De compacte schrijfwijze
(`20260903`) wordt geaccepteerd en genormaliseerd.

**`valid_from` mag nu ook in `sort_by` op `/products`.** De lijst van 27 augustus
wordt daarmee: `extracted_at`, `price`, `name`, `product_id`, `valid_from`.
Filteren op een startdag zonder erop te kunnen sorteren laat je alsnog blind
pagineren.

**Gecorrigeerd: `unit_price` bij Albert Heijn hoorde bij de reguliere prijs zodra
de actie een percentagekorting was.** Onze bron geeft de prijs per eenheid bij de
prijs vóór de korting; wij rekenden die alleen terug bij "2 voor …" en "1+1
gratis". Gemeld door een afnemer en gemeten op 3 september over alle lopende
acties met een korting én een prijs per eenheid: **831 van 2.607 rijen bij Albert
Heijn**, en **nul bij de andere negen ketens** — die leiden de stukprijs zelf uit
de actieprijs af. Voorbeeld: Amstel Pilsener 0,3 l voor €0,56 stond op €2,50/L
(dat is 0,75 / 0,3) en is nu €1,87/L. **`price`, `original_price` en `unit` zijn
ongewijzigd**, en er is geen veld bij of af — rekende je zelf al met
`price / quantity`, dan verandert er voor jou niets. De live rijen lopen mee met
de eerstvolgende nachtelijke scrape.

## 2026-09-02

**Nieuw: `promotion_status: "shelf"` — de reguliere prijs die een keten vandaag
rekent.** Tot nu toe kende `/match/*` drie waarden: `active`, `upcoming` en
`historical`. Er is er een vierde bij. Een `shelf`-rij is *geen* aanbieding —
`original_price`, `valid_from` en `valid_until` zijn `null` en `is_current_deal`
is `false` — maar het is wél wat je vandaag bij die keten betaalt.

**Filter je op een lijst statussen, vul die dan aan.** Dit is het enige dat je
integratie kan raken. Laat je onbekende waarden vallen, dan verlies je precies de
rijen met de meest actuele prijs; behandel je alles wat niet `active` is als
"verlopen", dan klopt dat voor `historical` en niet voor `shelf`.

**Wat er praktisch verandert.** Waar `/match/*` je eerder een `historical`-rij gaf
— de laatste prijs die wíj bij die keten zagen, tot zestig dagen oud — staat er nu
vaak een prijs van vandaag. Gemeten op 2 september over onze eigen
vergelijkkaarten: **1.514 producten krijgen zo'n rij, en bij 1.050 daarvan verving
hij een waarneming die tot twee maanden oud kon zijn.** Het maakt niet zozeer méér
producten vergelijkbaar — het maakt de prijs actueel op de producten die dat al
waren.

**Vandaag alleen PLUS.** Dat is een eigenschap van de bron en niet van het
endpoint: de meeste ketens publiceren alleen wat in de aanbieding is. Komt er een
keten bij, dan staat dat hier.

**Niet op `/search` en `/products`.** Daar houdt `promotion_status` zijn drie oude
waarden. Een schapprijs is geen aanbieding, dus hij staat niet tussen de acties —
je komt hem alleen tegen als vergelijkingsrij in `/match/*`.

**Geen schemawijziging** — geen veld erbij of eraf en `openapi.json` is
ongewijzigd, dus een gegenereerde client hoeft niet opnieuw. Wel nieuw:
[`examples/matching.py`](examples/matching.py), dat elke match met zijn status
print. De respons van `/match/*` staat in de spec als ongetypeerd object, dus dat
voorbeeld is de plek waar de veldnamen staan.

**Let op `best_deal` in `/match/compare/{ean}`:** dat is de laagste prijs ongeacht
status. Controleer daar `promotion_status` — nu ook op `shelf`.

## 2026-08-27 (2)

**Drie velden zijn uit het `/search`-antwoord verdwenen: `effective_unit_price`,
`unit_normalized` en `unit_price_raw`.** Alle drie stonden op **elk** product op
`null` — ze werden gevuld door een indexeerder die in de praktijk niet draaide.
Lees je ze uit, dan kreeg je dus al `null` en verandert er feitelijk niets; wel
verdwijnen ze uit `openapi.json`, dus **een gegenereerde client krijgt die drie
attributen niet meer**. Regenereer je client als je die uit de spec bouwt.

**De stukprijs zit in `unit_price`, met de eenheid in `unit`** (`kg`, `L` of
`stuk`). Die twee zijn ongewijzigd en gevuld op 62% van de producten. Reken je
zelf per eenheid, gebruik dan die twee — en let erop dat je alleen producten met
dezelfde `unit` onderling vergelijkt.

**Zoeksuggesties werken weer.** `/api/v1/suggest` gaf voor élke zoekterm een lege
lijst terug, met een `200`: het completion-veld waarop die endpoint zoekt, stond
niet in de index die daadwerkelijk gebouwd werd. Er waren drie definities van de
index en de laatste die draaide won. Dat is er nu één, en de suggesties komen
terug zodra de nachtelijke reindex is gelopen.

**Geen wijziging aan paden** — 24, ongewijzigd. Geen ander veld geraakt.

## 2026-08-27

**`sort_by` weigert nu een veld waarop niet gesorteerd kan worden, met een 422 in
plaats van een 500.** Op `/search` gaf een onbekend of niet-sorteerbaar veld een
serverfout — inclusief het voorbeeld dat in onze eigen documentatie stond
(`effective_unit_price:asc`) en de voor de hand liggende gok `name:asc`. Je krijgt
nu een 422 die de toegestane velden opsomt, en die lijst staat in de spec bij de
parameter zelf, zodat documentatie en gedrag niet meer uit elkaar kunnen lopen.

Toegestaan op `/search`: `price`, `savings_percentage`, `product_id`,
`savings_amount`, `original_price`, `discount_percentage`, `extracted_at`,
`valid_until` — elk optioneel met `:asc` of `:desc`. Op `/products`:
`extracted_at`, `price`, `name`, `product_id`.

**Wat dit voor je integratie betekent.** Gebruik je een van bovenstaande velden,
dan verandert er niets. Stuurde je een ander veld, dan kreeg je daarvoor een 500
(`/search`) of een willekeurig geordende pagina met een 200 (`/products`) — dat
laatste gaf met `page`/`page_size` eroverheen dubbele én ontbrekende rijen. Nu
zegt het antwoord wat er mis is.

`effective_unit_price` staat niet meer in de lijst met sorteervelden: dat veld is
op alle producten `null` en er kon dus nooit op gesorteerd worden. De stukprijs
zit in `unit_price` met `unit`.

**Geen wijziging aan paden of schema's.**

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
