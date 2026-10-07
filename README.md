# Supermarkt-API

Wekelijkse **supermarktaanbiedingen van 10 Nederlandse en 7 Belgische ketens** via
één REST-API, elke nacht ververst. Dit is de publieke documentatie, OpenAPI-specificatie en
voorbeeldcode bij de API van [PrijsProfeet](https://www.prijsprofeet.nl).

Geen enkele Nederlandse of Belgische supermarkt biedt een officiële publieke API. Deze wel — en
het grootste deel ervan werkt **zonder key en zonder registratie**.

```bash
curl -H 'User-Agent: MijnApp/1.0 (jij@voorbeeld.nl)' \
  'https://www.prijsprofeet.nl/api/v1/search?q=koffie&page_size=5'
```

Belgische aanbiedingen haal je met dezelfde API en dezelfde key bij
`https://www.prijsprofeet.be/api/v1/…`: de host bepaalt het land.

> **Wijzigingen volgen?** Zet deze repo op *Watch → Releases* — de knop rechtsboven,
> dan **Custom → Releases**. Elke wijziging die voor een integratie uitmaakt krijgt
> hier een release, met dezelfde tekst als het [changelog](CHANGELOG.md).

## Wat dit is — en wat het niet is

**Wel:** de promoties die deze week (en soms volgende week) lopen. Per product de
prijs, de van-prijs, de kortingsmechaniek, de geldigheidsdatum, de keten, een
categorie, dieetlabels en waar beschikbaar de EAN.

**Niet, op de gratis laag:** een volledig assortiment. Wat niet in de aanbieding is,
zit in de gratis endpoints niet. Bouw je een receptenapp of een boodschappenlijst-app,
reken daar dan op: van een willekeurig recept vind je meestal maar een deel van de
ingrediënten terug, en dat deel verschilt per week en per keten. Dit is de
belangrijkste reden dat een integratie tegenvalt, dus liever hier dan na twee weken
bouwen. De **reguliere prijs van het hele assortiment** (ook wat niet in de actie is)
staat in `GET /api/v1/shelf-prices`, op Pro.

## Ketens

**Nederland** (`www.prijsprofeet.nl/api/v1`): Albert Heijn · Aldi · DekaMarkt · Dirk ·
Ekoplaza · Hoogvliet · Jumbo · Lidl · PLUS · Vomar

**België** (`www.prijsprofeet.be/api/v1`): Albert Heijn · Aldi · Carrefour · Colruyt ·
Delhaize · Jumbo · Lidl

EAN-dekking verschilt per keten en is geen detail als je op product wilt koppelen.
Bij de meeste ketens staat er vrijwel altijd een EAN op een aanbieding. Bij een paar
publiceert de keten er zelf geen; daar koppelen we op naam, merk en verpakking, met de
foutmarge die daarbij hoort, en waar ook het merk ontbreekt koppelen we niet. Welke keten
waar valt verandert als een keten van bron wisselt, dus dat staat hier bewust niet: het
staat **gemeten** op
[prijsprofeet.nl](https://www.prijsprofeet.nl/supermarkt-aanbiedingen-api/#ketens) en
[prijsprofeet.be](https://www.prijsprofeet.be/supermarkt-aanbiedingen-api/#ketens), inclusief
de datum van de meting en welke ketens een reguliere schapprijs leveren.

## Beginnen

Geen key nodig voor zoeken, producten, aanbiedingen, categorieën en filterstatistieken:

| Endpoint | Doet |
|---|---|
| `GET /api/v1/search?q=` | Zoeken (fuzzy), gefilterd op categorie of dieetlabel |
| `GET /api/v1/products` | Bulk ophalen, pagineerbaar |
| `GET /api/v1/products/{id}` | Eén product, volledig |
| `GET /api/v1/deals/top?retailer=` | Topaanbiedingen, gegroepeerd per merk, optioneel per keten |
| `GET /api/v1/categories` | De categorieën, in groepen |

De volledige lijst staat in [`openapi.json`](openapi.json); werkende voorbeelden in
[`examples/`](examples/). ⚠️ De respons van `/match/*` staat in `openapi.json` als
ongetypeerd object — de parameters zijn daar volledig beschreven, de veldnamen niet.
Die staan in [`examples/matching.py`](examples/matching.py).

⚠️ **Let op `promotion_status`.** Er zijn vier waarden:

| Waarde | Betekent |
|---|---|
| `active` | de aanbieding loopt nu |
| `upcoming` | de aanbieding begint pas volgende week |
| `shelf` | geen aanbieding: de reguliere prijs die de keten vandaag rekent |
| `historical` | de laatste prijs die wij bij die keten zagen, maximaal 60 dagen oud |

Wie blind de laagste prijs pakt, toont een prijs die vandaag niet bestaat. Filter
erop, of gebruik `?current_only=true` waar dat wordt aangeboden. `shelf` komt alleen
voor in de respons van `/api/v1/match/*` en heeft geen van/voor-prijs en geen
`valid_from`/`valid_until`.

## Welk endpoint voor welke vraag

Bouw je een boodschappenplanner of prijsvergelijker, dan zit het antwoord vaak in een
veld of endpoint dat je niet meteen verwacht. Dit zijn de vragen die we het vaakst
terugzien.

| Vraag | Waar | Let op |
|---|---|---|
| Welke acties lopen er, allemaal? | `GET /api/v1/products/promotional/all`, eventueel met `?retailer=` | `total` is het aantal acties, niet de grootte van deze pagina: blader met `page` tot je ze allemaal hebt (`page_size` maximaal 100). `/search` sorteert op relevantie en is bedoeld om te zoeken, niet om een volledige lijst op te halen. |
| Wat kost een product buiten de actie? | `GET /api/v1/shelf-prices` (Pro), of de `"shelf"`-rijen in `/match/ean/{ean}` | Niet elke keten publiceert een reguliere prijs; welke wel, staat [per keten gemeten](https://www.prijsprofeet.nl/supermarkt-aanbiedingen-api/#ketens). |
| Wat betaal ik bij een actie op meer stuks? | `multi_buy_quantity` en `multi_buy_price` op elke actierij | `multi_buy_price` is het bedrag aan de kassa. `price` is de prijs per stuk, afgerond op de cent, dus vermenigvuldigen kan een cent afwijken. Bij Aldi (NL) is `price` zelf al het bundeltotaal. |
| Mag ik varianten van één actie combineren? | `promo_group_id`; `GET /api/v1/products?promo_group_id=…` geeft alle deelnemers | `promo_group_mixable` is alleen `true` of `false` als de keten het zelf zegt. `null` betekent "niet vermeld", niet "nee". |
| Geldt deze prijs nog in de winkel? | `valid_from`/`valid_until`, `extracted_at`, `valid_until_estimated`, `in_store_only`/`online_only`, `loyalty_price` | `valid_until` is de actieperiode, `extracted_at` wanneer wij de actie het laatst zagen. `valid_until_estimated: true` betekent dat wij de einddatum hebben ingeschat, omdat de keten er geen noemt. Een ledenprijs staat in `loyalty_price`, nooit in `price`. Op een schaprij: `price_changed_at` zegt sinds wanneer de prijs geldt. |
| Is dit hetzelfde product bij een andere keten? | `GET /api/v1/match/ean/{ean}` (Pro), met `?current_only=true` voor wat je vandaag kunt kopen | Eén EAN kan bij een keten meerdere verpakkingen dekken: vergelijk ook `quantity` en `unit_price`. |
| Welke velden staan alleen op productdetail? | `GET /api/v1/products/{id}` | `retailer_category`, `nutriscore` en `discount_percentage` staan niet in de zoekresultaten. |

## Gratis, Pro en Business

De **gratis laag heeft geen key nodig** en mag ook commercieel gebruikt worden, mits
je PrijsProfeet zichtbaar vermeldt (zie de
[API-voorwaarden](https://www.prijsprofeet.nl/api-voorwaarden)).

Drie dingen zitten achter een betaald plan: **cross-retailer EAN-matching**
(`/api/v1/match/*`), **reguliere schapprijzen** van het hele assortiment
(`/api/v1/shelf-prices`) en **prijsgeschiedenis per week**
(`/api/v1/products/{id}/price-history`). Een keten die deze week niets promoot valt
in een match niet weg: die krijgt zijn reguliere schapprijs mee (`promotion_status:
"shelf"`) in plaats van de laatste prijs die wij er zagen. Welke ketens dat vandaag zijn, staat
[per keten gemeten](https://www.prijsprofeet.nl/supermarkt-aanbiedingen-api/#ketens);
hier zou die lijst verouderen. Prijzen en een proefperiode van 14 dagen
staan op [prijsprofeet.nl/api](https://www.prijsprofeet.nl/api).

Een gratis key hoef je niet aan te vragen per mail — die haal je zelf op via
[prijsprofeet.nl/api](https://www.prijsprofeet.nl/api#gratis-key).

### Bronvermelding

Op Gratis en tijdens een proef vermeld je PrijsProfeet met een link, op elk scherm
waar onze data staat. Dit is genoeg:

```html
Aanbiedingen via <a href="https://www.prijsprofeet.nl">PrijsProfeet</a>
```

Gebruik je de Belgische data, link dan naar `https://www.prijsprofeet.be`. Staat je
product online, dan zetten we het graag op
[Gebouwd met PrijsProfeet](https://www.prijsprofeet.nl/gebouwd-met-prijsprofeet/), met
een gewone link naar je site.

## Limieten

| | Limiet |
|---|---|
| Zonder key | 30/min op bulk-endpoints, 120/min op zoeken en detail (maximaal 200 productdetails per dag) |
| Gratis key | 150/min, over alle endpoints samen |
| Pro / proef | 300/min |
| Business | 1.000/min |

Een gratis key is dus altijd ruimer dan helemaal geen key. Dat is bewust: wie zich
identificeert hoort er niet op achteruit te gaan.

## Noem jezelf in je User-Agent

Niet verplicht, wel netjes — en zonder key is het de enige manier waarop we je kunnen
bereiken bij een breaking change:

```
MijnApp/1.0 (+https://mijn-site.nl)
MijnApp/1.0 (jij@voorbeeld.nl)
```

⚠️ **Zet er geen `bot`, `crawler`, `spider` of `slurp` in.** Verzoeken *zonder* key met
zo'n User-Agent krijgen een `403`. Dat is anti-scrapebescherming, geen storing. Met een
key geldt de blokkade niet.

## OpenAPI

[`openapi.json`](openapi.json) is de complete specificatie (OpenAPI 3.1)
en is geschikt voor codegeneratie:

```bash
npx @openapitools/openapi-generator-cli generate \
  -i https://raw.githubusercontent.com/PrijsProfeet/supermarkt-api/main/openapi.json \
  -g python -o ./client
```

Er is ook een browsbare Swagger-UI op
[prijsprofeet.nl/docs](https://www.prijsprofeet.nl/docs), maar die is alleen in een
browser te openen — geautomatiseerde clients worden daar geblokkeerd. **Dit bestand is
de enige kopie die je machinaal kunt ophalen.**

## Wijzigingen

Nieuwe velden, nieuwe ketens en betere dekking rollen we zonder aankondiging uit.
**Breaking changes op een betaald endpoint kondigen we minimaal 30 dagen van tevoren
aan** — per e-mail aan betalende afnemers, en hier in [`CHANGELOG.md`](CHANGELOG.md).
Zet de repo op *Watch → Releases* als je dat wilt volgen.

## Vragen en problemen

- **Werkt iets niet, of klopt data niet?** Open een [issue](../../issues). Een
  verkeerd geclassificeerd product of een rare prijs is een prima issue — meldingen
  van gebruikers hebben de dataset al meermaals verbeterd.
- **"Hoe pak ik X aan?"** Gebruik [Discussions](../../discussions).
- **Zakelijk of over een plan?** info@prijsprofeet.nl

Deze repo bevat de documentatie, niet de scrapers of de API zelf.

## Voorwaarden

Op elk gebruik van de API — met of zonder key — zijn de
[API-voorwaarden](https://www.prijsprofeet.nl/api-voorwaarden) van toepassing. De kern:
je mag de data gebruiken en tonen, maar niet doorverkopen of er de dataset mee
namaken. De data is indicatief; controleer een prijs altijd bij de keten zelf.

De voorbeeldcode in deze repo staat onder de [MIT-licentie](LICENSE). Die licentie
geldt voor de code, niet voor de data.
