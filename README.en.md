# Supermarkt-API

[Nederlands](README.md) · **English**

Weekly **supermarket promotions from more than twenty Dutch and Belgian chains**, and from
Aldi Süd in Germany, through a single REST API, refreshed every night. This is the
public documentation, OpenAPI specification and example code for the API of [PrijsProfeet](https://www.prijsprofeet.nl).

Not a single Dutch or Belgian supermarket offers an official public API. This one does —
and most of it works **without a key and without registration**.

```bash
curl -H 'User-Agent: MyApp/1.0 (you@example.com)' \
  'https://www.prijsprofeet.nl/api/v1/search?q=koffie&page_size=5'
```

Belgian promotions come from the same API with the same key at
`https://www.prijsprofeet.be/api/v1/…`: the host decides the country. German offers
are on `https://www.prijsprofeet.de/api/v1/…`, for now from Aldi Süd only (see
[Chains](#chains)).

> **Want to follow changes?** Set this repo to *Watch → Releases* — the button at the top
> right, then **Custom → Releases**. You get one release a week with every change from the
> [changelog](CHANGELOG.md), and a release right away when you need to act (**Actie nodig**).

**Contents:** [What this is](#what-this-is--and-what-it-isnt) ·
[Chains](#chains) · [Getting started](#getting-started) ·
[Free, Pro and Business](#free-pro-and-business) ·
[Which endpoint for which question](#which-endpoint-for-which-question) · [Limits](#limits) ·
[User-Agent](#name-yourself-in-your-user-agent) · [OpenAPI](#openapi) · [MCP](#mcp-connector) · [Datasets](#datasets) · [Beta](#beta) ·
[Changes](#changes) · [Questions](#questions-and-problems) · [Terms](#terms)

## What this is — and what it isn't

**It is:** the promotions running this week (and sometimes next week). Per product the
price, the original price, the discount mechanism, the validity dates, the chain, a
category, dietary labels and, where available, the EAN.

**It is not, on the free tier:** a full assortment. Whatever isn't on promotion isn't in
the free endpoints. If you're building a recipe app or a shopping-list app, plan for that:
for any given recipe you will usually find only some of the ingredients, and which ones
differs per week and per chain. This is the main reason an integration disappoints, so
better to say it here than after two weeks of building. The **regular price of the full
assortment** (including what isn't on promotion) is in `GET /api/v1/shelf-prices`, and
that is a paid endpoint: see [Free, Pro and Business](#free-pro-and-business).

## Chains

**Netherlands** (`www.prijsprofeet.nl/api/v1`): Albert Heijn · Aldi · Amazing Oriental ·
Boni · Boon's Markt · Coop · Dagwinkel · DekaMarkt · Dirk · Ekoplaza · Gewoon Coop ·
Hoogvliet · Jumbo · Lidl · MCD · Nettorama · PLUS · Poiesz · SPAR · Vomar

**Belgium** (`www.prijsprofeet.be/api/v1`): Albert Heijn · Aldi · Carrefour · Colruyt ·
Delhaize · Jumbo · Lidl

**Germany** (`www.prijsprofeet.de/api/v1`): Aldi Süd. Germany is served per retailer: name
exactly one retailer in `retailer=aldi_sued` on `/search`, `/products` or `/products/changes`,
or use `/products/retailer/aldi_sued`. Other routes and requests without that retailer
return a 403. A product photo is only included as a link to the retailer itself. The
developer page is at [prijsprofeet.de/en/api](https://www.prijsprofeet.de/en/api).

EAN coverage differs per chain, and that is no detail if you want to match on product.
At most chains a promotion almost always carries an EAN. A few chains publish none
themselves; there we match on name, brand and pack size, with the margin of error that
comes with it, and where the brand is missing too we don't match. Which chain falls where
changes when a chain switches source, so it is deliberately not listed here: it is
**measured** on
[prijsprofeet.nl](https://www.prijsprofeet.nl/supermarkt-aanbiedingen-api/#ketens) and
[prijsprofeet.be](https://www.prijsprofeet.be/supermarkt-aanbiedingen-api/#ketens) (in Dutch),
including the date of the measurement and which chains provide a regular shelf price.

## Getting started

No key needed for search, products, promotions, categories and filter statistics:

| Endpoint | Does |
|---|---|
| `GET /api/v1/search?q=` | Search (fuzzy), filtered by category or dietary label |
| `GET /api/v1/products` | Bulk retrieval, paginated |
| `GET /api/v1/products/changes?cursor=` | Only what changed since your previous sync: new, changed or removed |
| `GET /api/v1/products/{id}` | One product, in full |
| `GET /api/v1/deals/top?retailer=` | Top promotions, grouped by brand, optionally per chain |
| `GET /api/v1/categories` | The categories, in groups |

The full list is in [`openapi.json`](openapi.json) ([`openapi.en.json`](openapi.en.json)
holds the same spec with English descriptions); working examples in
[`examples/`](examples/), without dependencies:

| Example | Shows |
|---|---|
| [`zoeken.py`](examples/zoeken.py) | `/search`, showing only what runs today |
| [`aanbiedingen_per_keten.py`](examples/aanbiedingen_per_keten.py) | `/deals/top` for one chain |
| [`product_detail.py`](examples/product_detail.py) | `/products/{id}` and why you match on EAN |
| [`matching.py`](examples/matching.py) | `/match/*` (Pro and Business), with the field names and the `min(price)` pitfall |
Call the API from your server. From a browser on another domain it does not work: the
API sends no CORS headers for other sites, and a key does not belong in a browser anyway.

⚠️ **Watch `promotion_status`.** There are four values:

| Value | Means |
|---|---|
| `active` | the promotion is running now |
| `upcoming` | the promotion only starts next week |
| `shelf` | no promotion: the regular price the chain charges today |
| `historical` | the last price we saw at that chain, at most 60 days old |

If you blindly take the lowest price, you show a price that doesn't exist today. Filter
on it, or use `?current_only=true` where it is offered. `shelf` only appears in the
response of `/api/v1/match/*` and has no original/promo price and no
`valid_from`/`valid_until`.

## Free, Pro and Business

| Plan | Key | What you get |
|---|---|---|
| **Free, without a key** | none | Search, products, promotions, categories, the change feed and the forecast. Limits per IP. |
| **Free, with a key** | [get it yourself](https://www.prijsprofeet.nl/api#gratis-key), in a minute | The same endpoints, with a higher limit on your key instead of on your IP. |
| **Pro** | on request, 14-day free trial | Everything in Free, plus EAN matching across chains (`/match/*`), shelf prices for the full assortment (`/shelf-prices`) and price history (`/products/{id}/price-history`). No attribution required. |
| **Business** | on request, annual contract | Everything in Pro, plus the shelf price series (`/shelf-prices/history`), private label equivalents (`/private-label-equivalents`), the highest limit and a 99.5% SLA. |

Prices are on [prijsprofeet.nl/api](https://www.prijsprofeet.nl/api) (in Dutch); here
they would go stale.

**Free may also be used commercially**, with or without a key, as long as you visibly
credit PrijsProfeet (see [Attribution](#attribution) and the
[API terms (in Dutch)](https://www.prijsprofeet.nl/api-voorwaarden)). A key costs nothing
and needs no email back-and-forth: enter your address on
[/api](https://www.prijsprofeet.nl/api#gratis-key), click the link in the email and your
key is on your screen.

A chain with no promotion this week does not drop out of a match: it comes with its
regular shelf price (`promotion_status: "shelf"`) instead of the last price we saw there.
Which chains provide a shelf price is
[measured per chain](https://www.prijsprofeet.nl/supermarkt-aanbiedingen-api/#ketens) (in Dutch).

### Attribution

On Free and during a trial you credit PrijsProfeet with a link, on every screen that
shows our data. Pick the snippet for the data you use and the language of your
product; this is enough:

```html
<!-- Dutch data -->
Aanbiedingen via <a href="https://www.prijsprofeet.nl">PrijsProfeet</a>

<!-- Belgian data, Dutch-language product -->
Promoties via <a href="https://www.prijsprofeet.be">PrijsProfeet</a>

<!-- Belgian data, French-language product -->
Promotions via <a href="https://www.prijsprofeet.be/fr/">PrijsProfeet</a>
```

The same snippets, with a copy button, are in
[your API account](https://www.prijsprofeet.nl/api-account/?lang=en#bronvermelding). If
your product is online, we're happy to list it on
[Gebouwd met PrijsProfeet](https://www.prijsprofeet.nl/gebouwd-met-prijsprofeet/) (in Dutch),
with a regular link to your site.

## Which endpoint for which question

If you're building a grocery planner or price comparison, the answer is often in a field
or endpoint you wouldn't expect at first. These are the questions we see most often.

Each endpoint lists which plans include it (see
[Free, Pro and Business](#free-pro-and-business)). A higher plan has everything of a
lower plan.

| Question | Where | Note |
|---|---|---|
| Which promotions are running, all of them? | `GET /api/v1/products/promotional/all`, optionally with `?retailer=` (all plans) | `total` is the number of promotions, not the size of this page: page through with `page` until you have them all (`page_size` at most 100). `/search` sorts by relevance and is meant for searching, not for fetching a complete list. |
| How do I keep my copy current without fetching everything every night? | `GET /api/v1/products/changes` (all plans) | First request a starting cursor (call without `cursor`), then sync once in full via `/api/v1/products`, and after that fetch only the changes: `upsert` replaces the row with that `product_id`, `delete` removes it. Store the `cursor` from each response and ask again right away while `has_more` is true. A change shows up within about ten minutes and is kept for 30 days; an older cursor returns a `410`, and then you sync in full again. Free, also without a key. |
| What does a product cost outside the promotion? | `GET /api/v1/shelf-prices`, or the `"shelf"` rows in `/match/ean/{ean}` (both Pro and Business) | Not every chain publishes a regular price; which ones do is [measured per chain](https://www.prijsprofeet.nl/supermarkt-aanbiedingen-api/#ketens) (in Dutch). |
| What do I pay for a multi-buy promotion? | `multi_buy_quantity` and `multi_buy_price` on every promotion row (all plans) | `multi_buy_price` is the amount at the till. `price` is the price per item, rounded to the cent, so multiplying can be a cent off. At Aldi (NL) `price` itself is already the bundle total. |
| May I combine variants of one promotion? | `promo_group_id`; `GET /api/v1/products?promo_group_id=…` returns all participants (all plans) | `promo_group_mixable` is only `true` or `false` if the chain says so itself. `null` means "not stated", not "no". |
| Does this price still apply in the store? | `valid_from`/`valid_until`, `extracted_at`, `valid_until_estimated`, `in_store_only`/`online_only`, `loyalty_price` (all plans) | `valid_until` is the promotion period, `extracted_at` when we last saw the promotion. `valid_until_estimated: true` means we estimated the end date because the chain doesn't state one. A member price is in `loyalty_price`, never in `price`. On a shelf row: `price_changed_at` says since when the price applies. |
| Is this the same product at another chain? | `GET /api/v1/match/ean/{ean}` (Pro and Business), with `?current_only=true` for what you can buy today; example in [`matching.py`](examples/matching.py) | One EAN can cover several pack sizes at a chain: compare `quantity` and `unit_price` as well. |
| What did this product cost before, and will it be on promotion again? | `GET /api/v1/products/{id}/price-history` (Pro and Business), `GET /api/v1/products/{id}/forecast` (all plans) | The history is a series per promotion week. If `/forecast` returns `null`, the `X-Forecast-Reason` header says why. |
| How did the regular price move? | `GET /api/v1/shelf-prices/history` (Business) | Every price movement per product, since we started tracking that chain (the first since September 2026). |
| Which private label is the same as another chain's? | `GET /api/v1/private-label-equivalents` (Business) | Where no barcode links them: same product and same pack size. |
| What does this recipe cost at each chain? | `POST /api/v1/match/ingredients` (beta; Pro and Business) | See [Recipe lines to shelf products](#recipe-lines-to-shelf-products). Always read the total per chain next to `lines_found` and `lines_total`. |
| How much of my limit have I used? | `GET /api/v1/partner/usage` (any key) | Also per day, and visible in your [API account](https://www.prijsprofeet.nl/api-account/). |
| Which fields are only on product detail? | `GET /api/v1/products/{id}` (all plans) | `retailer_category`, `nutriscore` and `discount_percentage` are not in the search results. |

## Limits

| | Limit |
|---|---|
| Without a key | 30/min on bulk endpoints, 120/min on search and detail (at most 200 product details and 500 searches on a bare EAN per day) |
| Free key | 150/min, across all endpoints combined |
| Pro / trial | 300/min |
| Business | 1,000/min |

So a free key is always more generous than no key at all. That is deliberate: identifying
yourself should never leave you worse off. A `429` carries `Retry-After`.

If your key is wrong (unknown or revoked), a request to a free endpoint is served as if it
had no key, at the lower limits, and the response carries the header
`X-PrijsProfeet-Notice`. If you suddenly see 429s, check that first. An endpoint that
requires a key answers a wrong key with a `403`. If your key cannot be looked up because
of an outage on our side, you get a `503` with `Retry-After`.

## Name yourself in your User-Agent

Not required, but courteous — and without a key it is the only way we can reach you
about a breaking change:

```
MyApp/1.0 (+https://my-site.example)
MyApp/1.0 (you@example.com)
```

⚠️ **Don't put `bot`, `crawler`, `spider` or `slurp` in it.** Requests *without* a key
with such a User-Agent may get a `403`. That is anti-scraping protection, not an outage. With
a key the block does not apply.

## OpenAPI

[`openapi.json`](openapi.json) is the complete specification (OpenAPI 3.1)
and is suitable for code generation; [`openapi.en.json`](openapi.en.json) holds the same
spec with English descriptions:

```bash
npx @openapitools/openapi-generator-cli generate \
  -i https://raw.githubusercontent.com/PrijsProfeet/supermarkt-api/main/openapi.json \
  -g python -o ./client
```

There is also a browsable Swagger UI at
[prijsprofeet.nl/docs/en](https://www.prijsprofeet.nl/docs/en), but it can only be opened
in a browser — automated clients are blocked there. **This file is the only copy you can
fetch programmatically.**

## MCP connector

Besides the REST API there is an **MCP server** for AI assistants and agents, with no
key and no registration.

| | |
|---|---|
| Netherlands | `https://www.prijsprofeet.nl/api/v1/mcp` |
| Belgium | `https://www.prijsprofeet.be/api/v1/mcp` |
| Germany | `https://www.prijsprofeet.de/api/v1/mcp` |
| Transport | Streamable HTTP, POST only (a GET answers `405`) |
| Authentication | none |

The host decides the country, as with the API. To add it as a user in Claude or
ChatGPT, see the steps (in Dutch) at
[prijsprofeet.nl/chatgpt-en-claude](https://www.prijsprofeet.nl/chatgpt-en-claude/); it
is listed in the directory of Claude (Netherlands, Belgium and Germany) and ChatGPT
(Netherlands and Belgium).

**What it is for.** The connector answers a user's question: where a product is on
offer this week, where it is cheapest right now, what it normally costs. The answer is
short text (in Dutch) with a link to the page it came from, not raw rows, not EANs and
not full price series. **If you are building your own product or app, use the
[REST API](#getting-started)**; the connector is not a keyless route to the same data.

**Tools**

| Tool | What |
|---|---|
| `search` | Search by product or brand name. Returns brand pages and products, each with an `id`. An EAN is not accepted as a query. |
| `fetch` | Fetch a result by its `id`. |

| Id | Returns |
|---|---|
| `merk:{slug}` | A brand's offers, running ones first, then upcoming ones, each cheapest first |
| `merk:{slug}:{n}` | Page `n` of those; the answer names the id of the next page as long as there are more |
| `product:{id}` | Price, validity, lowest promotional price of the past six months, and the price at other supermarkets |
| `schap:{zoekterm}` | Per supermarket the cheapest regular price, also without a promotion |

Use the ids that `search` returns; building them yourself works, but the format may
change. An ended promotion returns an answer saying so (with the regular price if the
chain still charges one), an unknown id returns an error.

**Limits.** Clients other than Claude and ChatGPT share a daily limit. When it is used
up, the answer says so and points to the API. If you need more, the API with a (free)
key is the way.

**Attribution.** Every answer carries a source line with a link; keep it when you show
the answer to a user. The [API terms](https://www.prijsprofeet.nl/api-voorwaarden) apply
here too.

## Datasets

Prefer a file over an API? The [PrijsProfeet Datasets](https://www.prijsprofeet.nl/en/datasets/)
are fixed snapshots of our Dutch price data as CSV: shelf prices with every price change,
and promotions with label and validity, with a datasheet and a licence. A dataset is a
copy you may keep under the licence; the API gives access and asks you to delete the data
when your plan ends ([terms](https://www.prijsprofeet.nl/api-voorwaarden)). There is a
[free sample](https://www.prijsprofeet.nl/en/datasets/#voorbeeld) and a special rate for
universities and research institutions.

## Beta

Beta features fall outside the SLA and may change without the 30-day notice
([terms, art. 10, in Dutch](https://www.prijsprofeet.nl/api-voorwaarden#beta)). You switch
them on in your [API account](https://www.prijsprofeet.nl/api-account/), under *Bèta*, and
give feedback there too. Currently in beta:

- [Recipe lines to shelf products](#recipe-lines-to-shelf-products): send the lines of a
  recipe or shopping list and get the matching product at each chain.

The [notification after the nightly run](#notification-after-the-nightly-run) was in beta
until 5 November 2026 and is now part of the regular API.

### Recipe lines to shelf products

Want to know what the ingredients of a recipe or a shopping list cost at each chain? Send
the lines in one request. For each line and chain you get the product that fits best, at
its regular shelf price, plus two alternatives:

```bash
curl -X POST https://www.prijsprofeet.nl/api/v1/match/ingredients \
  -H "X-API-Key: $PRIJSPROFEET_KEY" -H "Content-Type: application/json" \
  -d '{"lines": ["2 uien", "500 g spaghetti", {"name": "tenen knoflook", "value": 4, "unitCode": "H87"}]}'
```

```json
{
  "country": "nl",
  "valid_until": "2026-11-06T04:30:00+01:00",
  "lines_counted": 3,
  "lines": [
    {
      "index": 0,
      "line": "2 uien",
      "status": "found",
      "optional": false,
      "interpreted": {"terms": ["uien"], "amount": {"value": 2.0, "unit": "stuk"}, "organic": false},
      "retailers": {
        "albert_heijn": [
          {"name": "AH Gele uien", "brand": "AH", "quantity": "3 stuks",
           "pack_size": {"value": 3.0, "unit": "stuk"}, "price": 0.89,
           "unit_price": 0.3, "unit": "stuk", "packs": 1, "line_price": 0.89,
           "shelf_id": "525847", "ean": "8718907615778", "product_url": "…", "image_url": "…"}
        ]
      }
    }
  ],
  "retailers": [
    {"retailer": "albert_heijn", "name": "Albert Heijn", "lines_found": 3, "lines_total": 3, "total_price": 2.72}
  ],
  "retailers_without_shelf_prices": ["lidl"]
}
```

Shortened to one line and one chain; prices of 5 November 2026.

**Lines are Dutch.** A line is text (`"500 g spaghetti"`, `"1 blik tomatenblokjes"`) or an
object shaped like schema.org `PropertyValue`: `name`, `value`, `unitCode`, plus optional
`note` (not searched) and `optional`. As `unitCode` use `GRM`, `KGM`, `MLT`, `LTR` or `H87`
(pieces), or the kitchen measures `el`, `tl` and `snufje`. Put any other measure in the name
with `H87`: `{"name": "tenen knoflook", "value": 4, "unitCode": "H87"}`. An unknown
`unitCode` returns a `422` that names the line.

**How we count.** For a weight, volume or number we pick the pack closest to the amount
asked, rounded up to whole packs (`packs`). A kitchen measure (`el`, `teen`, `takje`,
`snufje`) says nothing about what you buy: then we take the smallest pack once, and
`amount` is `null`. So "4 tenen knoflook" is one pack of garlic. Without the word "tenen"
we read 4 pieces of garlic.

**Is this pack bigger than I need?** That is your call, with `pack_size`: the pack size as
a number, in the same unit as `interpreted.amount`, and `null` when the chain states no
readable size. Divide it by the amount asked for and pick your own threshold. We attach no
flag of our own, and that is a measurement: over 1,643 products reviewed by test partners, a
pack is at least twice the amount asked for in 55% of cases, and nine times out of ten that
is simply the normal pack — a litre of sunflower oil for 15 ml is how oil is sold. A warning
from us would therefore sit on more than half of your lines and be wrong most of the time.

**A form that needs a machine is dropped.** A line asking for coffee or espresso returns no
capsules, cups or pads, and no ready-to-drink coffee with milk or sugar; ground coffee,
instant coffee and beans stay, and so does a can without sugar and without milk. If the line
itself asks for that form ("20 koffiecapsules"), you do get it. The same holds for bread: a
line asking for bread returns no baguette or roll unless you ask for one.

**The total** per chain is the sum of `line_price` over the lines found. Always read it next
to `lines_found` out of `lines_total`: a total over 7 of 12 lines is not a basket price.
Optional lines and what is not for sale (`"status": "not_for_sale"`, such as tap water) do
not count. Chains without shelf prices are in `retailers_without_shelf_prices`.

**Limits.** At most 50 lines per request and 10,000 distinct lines per key per day. The
same line twice in one request counts once; it appears twice in the answer and the total.
Whether you send lines in one request or one by one makes no difference to the daily limit.
One request is faster, though, and the per-minute limit counts requests.

**Caching.** Prices are refreshed every night. An answer stays valid until `valid_until`:
cache it until then, per recipe. That way you pay per recipe, not per visitor.

**Privacy.** A list can say something about a person. Send the lines only in the body, from
your server. We do not store them and they appear in no log. We only count how many.

Only on `www.prijsprofeet.nl`: the matching is measured on Dutch lines. For Pro and
Business, and for a Pro trial. Sign up in your
[API account](https://www.prijsprofeet.nl/api-account/), under *Bèta*. This feature needs
permission: after you sign up, we switch it on for you. Without sign-up the route returns a
`403`.

## Notification after the nightly run

Want to know when last night's data is in, instead of syncing on a guess? Switch it on in your
[API account](https://www.prijsprofeet.nl/api-account/), with your key, and provide an
https URL. Every morning around 07:05, after our freshness measurement, we send one POST
there:

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

`fresh` is the same freshness measurement as on [status.prijsprofeet.nl](https://status.prijsprofeet.nl):
that chain's promotions were refreshed last night and are complete. The notification lists
every chain of both storefronts; filter on `country` if you only use one.

**Verify the signature.** Every notification carries the headers `webhook-id`,
`webhook-timestamp` and `webhook-signature`, following
[Standard Webhooks](https://www.standardwebhooks.com/). The secret (`whsec_…`) is in your
account. Any Standard Webhooks or Svix library can verify it, or do it yourself:

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

Also check that `webhook-timestamp` is no older than a few minutes.

**What we expect:** a 2xx within 10 seconds. We don't follow redirects. If it fails, we
retry after 1, 5 and 30 minutes. After 5 consecutive nights without a successful
notification we switch it off; you'll see that in your account and can switch it back on
there. *Testmelding sturen* (send test notification) in your account sends you a
notification with `"test": true` right away.

Available on every plan. Since 5 November 2026 the notification is no longer a beta: we
announce a breaking change 30 days in advance ([art. 10, in Dutch](https://www.prijsprofeet.nl/api-voorwaarden)).

## Changes

New fields, new chains and better coverage are rolled out without announcement.
**Breaking changes on a paid endpoint are announced at least 30 days in advance** — by
email to paying customers, and here in [`CHANGELOG.md`](CHANGELOG.md). Set the repo to
*Watch → Releases* if you want to follow that.

## Questions and problems

- **Something not working, or data wrong?** Open an [issue](../../issues). A
  misclassified product or an odd price is a fine issue — user reports have improved the
  dataset several times already.
- **"How do I approach X?"** Use [Discussions](../../discussions).
- **Which plan fits?** The plans and prices are on [prijsprofeet.nl/api](https://www.prijsprofeet.nl/api) (in Dutch);
  request a trial or Business there. Anything else business-related: info@prijsprofeet.nl.

This repo contains the documentation, not the scrapers or the API itself.

## Terms

Every use of the API — with or without a key — is subject to the
[API terms (in Dutch)](https://www.prijsprofeet.nl/api-voorwaarden). The gist: you may
use and display the data, but not resell it or use it to recreate the dataset. The data
is indicative; always check a price with the chain itself.

Every version of the terms is also in this repo. The current one is in
[API terms (in Dutch)](voorwaarden/api-voorwaarden.md), earlier ones (1.0 through 1.13) in
[`voorwaarden/eerder/`](voorwaarden/eerder/), and from 1.14 onwards the
[history of the file](https://github.com/PrijsProfeet/supermarkt-api/commits/main/voorwaarden/api-voorwaarden.md)
shows every change. The version on the site is binding.

The Dutch text of the API terms is the binding version; this README is a translation for convenience.

The example code in this repo is under the [MIT license](LICENSE). That license applies
to the code, not to the data.
