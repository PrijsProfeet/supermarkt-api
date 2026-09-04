# Supermarkt-API

Wekelijkse **supermarktaanbiedingen van 10 Nederlandse ketens** via één REST-API,
elke nacht ververst. Dit is de publieke documentatie, OpenAPI-specificatie en
voorbeeldcode bij de API van [PrijsProfeet](https://www.prijsprofeet.nl).

Geen enkele Nederlandse supermarkt biedt een officiële publieke API. Deze wel — en
het grootste deel ervan werkt **zonder key en zonder registratie**.

```bash
curl -H 'User-Agent: MijnApp/1.0 (jij@voorbeeld.nl)' \
  'https://www.prijsprofeet.nl/api/v1/search?q=koffie&page_size=5'
```

> **Wijzigingen volgen?** Zet deze repo op *Watch → Releases* — de knop rechtsboven,
> dan **Custom → Releases**. Elke wijziging die voor een integratie uitmaakt krijgt
> hier een release, met dezelfde tekst als het [changelog](CHANGELOG.md).

## Wat dit is — en wat het niet is

**Wel:** de promoties die deze week (en soms volgende week) lopen. Per product de
prijs, de van-prijs, de kortingsmechaniek, de geldigheidsdatum, de keten, een
categorie, dieetlabels en waar beschikbaar de EAN.

**Niet:** een volledig assortiment. Wat niet in de aanbieding is, zit er niet in.
Bouw je een receptenapp of een boodschappenlijst-app, reken daar dan op: van een
willekeurig recept vind je meestal maar een deel van de ingrediënten terug, en dat
deel verschilt per week en per keten. Dit is de belangrijkste reden dat een
integratie tegenvalt, dus liever hier dan na twee weken bouwen.

## Ketens

Albert Heijn · Aldi · DekaMarkt · Dirk · Ekoplaza · Hoogvliet · Jumbo · Lidl ·
PLUS · Vomar

EAN-dekking verschilt per keten en is geen detail als je op product wilt koppelen:
bij **Albert Heijn, Jumbo, Dirk en DekaMarkt** is de EAN er vrijwel altijd, bij
**Aldi, Lidl, Hoogvliet en Vomar publiceert de keten zelf geen EAN** — daar bestaat
hij domweg niet. Koppelen op naam is dan de enige optie, met de foutmarge die daarbij
hoort.

## Beginnen

Geen key nodig voor zoeken, producten, aanbiedingen, categorieën en filterstatistieken:

| Endpoint | Doet |
|---|---|
| `GET /api/v1/search?q=` | Zoeken (fuzzy), gefilterd op categorie of dieetlabel |
| `GET /api/v1/products` | Bulk ophalen, pagineerbaar |
| `GET /api/v1/products/{id}` | Eén product, volledig |
| `GET /api/v1/deals/top?retailer=` | Topaanbiedingen, gegroepeerd per merk, optioneel per keten |
| `GET /api/v1/categories` | De 18 categorieën |

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

## Gratis, Pro en Business

De **gratis laag heeft geen key nodig** en mag ook commercieel gebruikt worden, mits
je PrijsProfeet zichtbaar vermeldt (zie de
[API-voorwaarden](https://www.prijsprofeet.nl/api-voorwaarden)).

Twee dingen zitten achter een betaald plan: **cross-retailer EAN-matching**
(`/api/v1/match/*`) en **prijsgeschiedenis per week**
(`/api/v1/products/{id}/price-history`). Een keten die deze week niets promoot valt
in een match niet weg: die krijgt zijn reguliere schapprijs mee (`promotion_status:
"shelf"`) in plaats van de laatste prijs die wij er zagen. Vandaag leveren PLUS,
Dirk en DekaMarkt die. Prijzen en een proefperiode van 14 dagen
staan op [prijsprofeet.nl/api](https://www.prijsprofeet.nl/api).

Een gratis key hoef je niet aan te vragen per mail — die haal je zelf op via
[prijsprofeet.nl/api](https://www.prijsprofeet.nl/api#gratis-key).

## Limieten

| | Limiet |
|---|---|
| Zonder key | 30/min op bulk-endpoints, 120/min op zoeken en detail |
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

[`openapi.json`](openapi.json) is de complete specificatie (OpenAPI 3.1, 24 endpoints)
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
