# Supermarkt-API

Wekelijkse **supermarktaanbiedingen van meer dan twintig Nederlandse en Belgische
ketens** via één REST-API, elke nacht ververst. Dit is de publieke documentatie, OpenAPI-specificatie en
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

**Inhoud:** [Wat dit is](#wat-dit-is--en-wat-het-niet-is) ·
[Ketens](#ketens) · [Beginnen](#beginnen) ·
[Welk endpoint voor welke vraag](#welk-endpoint-voor-welke-vraag) ·
[Gratis, Pro en Business](#gratis-pro-en-business) · [Limieten](#limieten) ·
[User-Agent](#noem-jezelf-in-je-user-agent) · [OpenAPI](#openapi) · [Bèta](#bèta) ·
[Wijzigingen](#wijzigingen) · [Vragen](#vragen-en-problemen) · [Voorwaarden](#voorwaarden)

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
staat in `GET /api/v1/shelf-prices`, en dat is een betaald endpoint: zie
[Gratis, Pro en Business](#gratis-pro-en-business).

## Ketens

**Nederland** (`www.prijsprofeet.nl/api/v1`): Albert Heijn · Aldi · Boon's Markt ·
DekaMarkt · Dirk · Ekoplaza · Gewoon Coop · Hoogvliet · Jumbo · Lidl · MCD · Nettorama ·
PLUS · Poiesz · SPAR · Vomar

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
| `GET /api/v1/products/changes?cursor=` | Alleen wat er sinds je vorige sync veranderde: nieuw, gewijzigd of verdwenen |
| `GET /api/v1/products/{id}` | Eén product, volledig |
| `GET /api/v1/deals/top?retailer=` | Topaanbiedingen, gegroepeerd per merk, optioneel per keten |
| `GET /api/v1/categories` | De categorieën, in groepen |

De volledige lijst staat in [`openapi.json`](openapi.json); werkende voorbeelden in
[`examples/`](examples/), zonder dependencies:

| Voorbeeld | Laat zien |
|---|---|
| [`zoeken.py`](examples/zoeken.py) | `/search`, en alleen tonen wat vandaag loopt |
| [`aanbiedingen_per_keten.py`](examples/aanbiedingen_per_keten.py) | `/deals/top` voor één keten |
| [`product_detail.py`](examples/product_detail.py) | `/products/{id}` en waarom je op EAN koppelt |
| [`matching.py`](examples/matching.py) | `/match/*` (Pro), met de veldnamen en de `min(price)`-valkuil |
 ⚠️ De respons van `/match/*` staat in `openapi.json` als
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

Achter elk endpoint staat welk plan je nodig hebt (zie
[Gratis, Pro en Business](#gratis-pro-en-business)).

| Vraag | Waar | Let op |
|---|---|---|
| Welke acties lopen er, allemaal? | `GET /api/v1/products/promotional/all`, eventueel met `?retailer=` (Gratis) | `total` is het aantal acties, niet de grootte van deze pagina: blader met `page` tot je ze allemaal hebt (`page_size` maximaal 100). `/search` sorteert op relevantie en is bedoeld om te zoeken, niet om een volledige lijst op te halen. |
| Hoe houd ik mijn kopie actueel zonder elke nacht alles op te halen? | `GET /api/v1/products/changes` (Gratis) | Vraag eerst een startcursor op (aanroep zonder `cursor`), synchroniseer dan één keer volledig via `/api/v1/products`, en haal daarna alleen de wijzigingen op: `upsert` vervangt de rij met die `product_id`, `delete` haalt hem weg. Bewaar de `cursor` uit elk antwoord en vraag meteen opnieuw zolang `has_more` waar is. Een wijziging staat er binnen ongeveer tien minuten in en blijft 30 dagen bewaard; een oudere cursor geeft een `410` en dan synchroniseer je opnieuw volledig. Gratis, ook zonder key. |
| Wat kost een product buiten de actie? | `GET /api/v1/shelf-prices` (Pro), of de `"shelf"`-rijen in `/match/ean/{ean}` | Niet elke keten publiceert een reguliere prijs; welke wel, staat [per keten gemeten](https://www.prijsprofeet.nl/supermarkt-aanbiedingen-api/#ketens). |
| Wat betaal ik bij een actie op meer stuks? | `multi_buy_quantity` en `multi_buy_price` op elke actierij (Gratis) | `multi_buy_price` is het bedrag aan de kassa. `price` is de prijs per stuk, afgerond op de cent, dus vermenigvuldigen kan een cent afwijken. Bij Aldi (NL) is `price` zelf al het bundeltotaal. |
| Mag ik varianten van één actie combineren? | `promo_group_id`; `GET /api/v1/products?promo_group_id=…` geeft alle deelnemers (Gratis) | `promo_group_mixable` is alleen `true` of `false` als de keten het zelf zegt. `null` betekent "niet vermeld", niet "nee". |
| Geldt deze prijs nog in de winkel? | `valid_from`/`valid_until`, `extracted_at`, `valid_until_estimated`, `in_store_only`/`online_only`, `loyalty_price` (Gratis) | `valid_until` is de actieperiode, `extracted_at` wanneer wij de actie het laatst zagen. `valid_until_estimated: true` betekent dat wij de einddatum hebben ingeschat, omdat de keten er geen noemt. Een ledenprijs staat in `loyalty_price`, nooit in `price`. Op een schaprij: `price_changed_at` zegt sinds wanneer de prijs geldt. |
| Is dit hetzelfde product bij een andere keten? | `GET /api/v1/match/ean/{ean}` (Pro), met `?current_only=true` voor wat je vandaag kunt kopen; voorbeeld in [`matching.py`](examples/matching.py) | Eén EAN kan bij een keten meerdere verpakkingen dekken: vergelijk ook `quantity` en `unit_price`. |
| Wat kostte dit product eerder, en komt het terug in de actie? | `GET /api/v1/products/{id}/price-history` (Pro), `GET /api/v1/products/{id}/forecast` (Gratis) | De geschiedenis is een reeks per actieweek. Geeft `/forecast` `null`, dan zegt de header `X-Forecast-Reason` waarom. |
| Hoe bewoog de reguliere prijs? | `GET /api/v1/shelf-prices/history` (Business) | Elke prijsbeweging per product, sinds we die keten volgen (de eerste sinds september 2026). |
| Welk huismerk is hetzelfde als dat van een andere keten? | `GET /api/v1/private-label-equivalents` (Business) | Waar geen barcode ze koppelt: zelfde product én zelfde verpakking. |
| Hoeveel van mijn limiet heb ik gebruikt? | `GET /api/v1/partner/usage` (elke key) | Ook per dag, en te zien in je [API-account](https://www.prijsprofeet.nl/api-account/). |
| Welke velden staan alleen op productdetail? | `GET /api/v1/products/{id}` (Gratis) | `retailer_category`, `nutriscore` en `discount_percentage` staan niet in de zoekresultaten. |

## Gratis, Pro en Business

| Plan | Key | Wat je krijgt |
|---|---|---|
| **Gratis, zonder key** | geen | Zoeken, producten, aanbiedingen, categorieën, de change feed en de voorspelling. Limieten per IP. |
| **Gratis, met key** | [zelf ophalen](https://www.prijsprofeet.nl/api#gratis-key), in een minuut | Dezelfde endpoints, met een ruimere limiet op je key in plaats van op je IP. |
| **Pro** | op aanvraag, 14 dagen gratis te proberen | Alles uit Gratis, plus EAN-matching over ketens (`/match/*`), schapprijzen van het hele assortiment (`/shelf-prices`) en prijsgeschiedenis (`/products/{id}/price-history`). Geen bronvermelding verplicht. |
| **Business** | op aanvraag, jaarcontract | Alles uit Pro, plus de schapprijsreeks (`/shelf-prices/history`), huismerk-equivalenten (`/private-label-equivalents`), de hoogste limiet en een SLA van 99,5%. |

Prijzen staan op [prijsprofeet.nl/api](https://www.prijsprofeet.nl/api); hier zouden
ze verouderen.

**Gratis mag ook commercieel**, met of zonder key, zolang je PrijsProfeet zichtbaar
vermeldt (zie [Bronvermelding](#bronvermelding) en de
[API-voorwaarden](https://www.prijsprofeet.nl/api-voorwaarden)). Een key kost niets en
vraagt geen mailwisseling: je vult op [/api](https://www.prijsprofeet.nl/api#gratis-key)
je adres in, klikt de link in de mail aan en je key staat op je scherm.

Een keten die deze week niets promoot valt in een match niet weg: die krijgt zijn
reguliere schapprijs mee (`promotion_status: "shelf"`) in plaats van de laatste prijs
die wij er zagen. Welke ketens een schapprijs leveren, staat
[per keten gemeten](https://www.prijsprofeet.nl/supermarkt-aanbiedingen-api/#ketens).

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
| Zonder key | 30/min op bulk-endpoints, 120/min op zoeken en detail (maximaal 200 productdetails en 500 zoekopdrachten op een kale EAN per dag) |
| Gratis key | 150/min, over alle endpoints samen |
| Pro / proef | 300/min |
| Business | 1.000/min |

Een gratis key is dus altijd ruimer dan helemaal geen key. Dat is bewust: wie zich
identificeert hoort er niet op achteruit te gaan. Een `429` draagt `Retry-After`.

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

## Bèta

Bètafuncties vallen buiten de SLA en kunnen veranderen zonder de aankondiging van 30
dagen ([voorwaarden, art. 10](https://www.prijsprofeet.nl/api-voorwaarden#beta)). Je zet
ze aan in je [API-account](https://www.prijsprofeet.nl/api-account/), onder *Bèta*, en
geeft daar ook feedback. Nu in bèta:

- [Melding na de nachtrun](#melding-na-de-nachtrun): één webhook per ochtend zodra de
  data van vannacht er staat.

### Melding na de nachtrun

Wil je weten wanneer de data van vannacht er staat, in plaats van op de gok te
synchroniseren? Meld je aan in je
[API-account](https://www.prijsprofeet.nl/api-account/), onder *Bèta*, en geef een
https-URL op. Elke ochtend rond 07:05, na onze versheidsmeting, sturen we daar één
POST naartoe:

```json
{
  "type": "nachtrun.gemeten",
  "test": false,
  "day": "2026-10-10",
  "chains": [
    {"retailer": "albert_heijn", "name": "Albert Heijn", "country": "nl", "fresh": true},
    {"retailer": "jumbo", "name": "Jumbo", "country": "nl", "fresh": false}
  ]
}
```

`fresh` is dezelfde versheidsmeting als op [status.prijsprofeet.nl](https://status.prijsprofeet.nl):
de acties van die keten zijn vannacht ververst en compleet. De melding noemt elke keten van beide
winkels; filter op `country` als je er maar één gebruikt.

**Controleer de handtekening.** Elke melding draagt de headers `webhook-id`,
`webhook-timestamp` en `webhook-signature`, volgens
[Standard Webhooks](https://www.standardwebhooks.com/). Het geheim (`whsec_…`) staat in je
account. Elke Standard Webhooks- of Svix-bibliotheek kan hem controleren, of zelf:

```python
import base64, hashlib, hmac

def is_echt(secret: str, headers: dict, body: bytes) -> bool:
    key = base64.b64decode(secret.removeprefix("whsec_"))
    signed = f"{headers['webhook-id']}.{headers['webhook-timestamp']}.".encode() + body
    expected = base64.b64encode(hmac.new(key, signed, hashlib.sha256).digest()).decode()
    return any(
        hmac.compare_digest(sig.partition(",")[2], expected)
        for sig in headers["webhook-signature"].split()
    )
```

Controleer ook dat `webhook-timestamp` niet ouder is dan een paar minuten.

**Wat we verwachten:** een 2xx binnen 10 seconden. Een doorverwijzing volgen we niet.
Lukt het niet, dan proberen we het na 1, 5 en 30 minuten opnieuw. Na 5 nachten op rij
zonder geslaagde melding zetten we hem uit; je ziet dat in je account en zet hem daar
weer aan. Met *Testmelding sturen* in je account krijg je meteen een melding met
`"test": true`.

Op dit moment voor Gratis en de Pro-proef.

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
- **Welk plan past?** De plannen en prijzen staan op [prijsprofeet.nl/api](https://www.prijsprofeet.nl/api);
  een proef of Business vraag je daar aan. Iets anders zakelijks: info@prijsprofeet.nl.

Deze repo bevat de documentatie, niet de scrapers of de API zelf.

## Voorwaarden

Op elk gebruik van de API — met of zonder key — zijn de
[API-voorwaarden](https://www.prijsprofeet.nl/api-voorwaarden) van toepassing. De kern:
je mag de data gebruiken en tonen, maar niet doorverkopen of er de dataset mee
namaken. De data is indicatief; controleer een prijs altijd bij de keten zelf.

Elke versie van de voorwaarden staat ook in deze repo, in
[`voorwaarden/api-voorwaarden.md`](voorwaarden/api-voorwaarden.md): de
[geschiedenis van dat bestand](https://github.com/PrijsProfeet/supermarkt-api/commits/main/voorwaarden/api-voorwaarden.md)
laat zien wat er op een eerdere datum gold. Bindend is de versie op de site.

De voorbeeldcode in deze repo staat onder de [MIT-licentie](LICENSE). Die licentie
geldt voor de code, niet voor de data.
