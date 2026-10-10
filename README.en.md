# Supermarkt-API

[Nederlands](README.md) · **English**

Weekly **supermarket promotions from more than twenty Dutch and Belgian chains** through
a single REST API, refreshed every night. This is the public documentation, OpenAPI
specification and example code for the API of [PrijsProfeet](https://www.prijsprofeet.nl).

Not a single Dutch or Belgian supermarket offers an official public API. This one does —
and most of it works **without a key and without registration**.

```bash
curl -H 'User-Agent: MyApp/1.0 (you@example.com)' \
  'https://www.prijsprofeet.nl/api/v1/search?q=koffie&page_size=5'
```

Belgian promotions come from the same API with the same key at
`https://www.prijsprofeet.be/api/v1/…`: the host decides the country.

> **Want to follow changes?** Set this repo to *Watch → Releases* — the button at the top
> right, then **Custom → Releases**. Every change that matters to an integration gets a
> release here, with the same text as the [changelog](CHANGELOG.md).

**Contents:** [What this is](#what-this-is--and-what-it-isnt) ·
[Chains](#chains) · [Getting started](#getting-started) ·
[Free, Pro and Business](#free-pro-and-business) ·
[Which endpoint for which question](#which-endpoint-for-which-question) · [Limits](#limits) ·
[User-Agent](#name-yourself-in-your-user-agent) · [OpenAPI](#openapi) · [Beta](#beta) ·
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

**Netherlands** (`www.prijsprofeet.nl/api/v1`): Albert Heijn · Aldi · Boon's Markt ·
DekaMarkt · Dirk · Ekoplaza · Gewoon Coop · Hoogvliet · Jumbo · Lidl · MCD · Nettorama ·
PLUS · Poiesz · SPAR · Vomar

**Belgium** (`www.prijsprofeet.be/api/v1`): Albert Heijn · Aldi · Carrefour · Colruyt ·
Delhaize · Jumbo · Lidl

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
 ⚠️ The response of `/match/*` is in `openapi.json` as an
untyped object — the parameters are fully described there, the field names are not.
Those are in [`examples/matching.py`](examples/matching.py).

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
shows our data. This is enough:

```html
Aanbiedingen via <a href="https://www.prijsprofeet.nl">PrijsProfeet</a>
```

If you use the Belgian data, link to `https://www.prijsprofeet.be`. If your product is
online, we're happy to list it on
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

## Name yourself in your User-Agent

Not required, but courteous — and without a key it is the only way we can reach you
about a breaking change:

```
MyApp/1.0 (+https://my-site.example)
MyApp/1.0 (you@example.com)
```

⚠️ **Don't put `bot`, `crawler`, `spider` or `slurp` in it.** Requests *without* a key
with such a User-Agent get a `403`. That is anti-scraping protection, not an outage. With
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

## Beta

Beta features fall outside the SLA and may change without the 30-day notice
([terms, art. 10, in Dutch](https://www.prijsprofeet.nl/api-voorwaarden#beta)). You switch
them on in your [API account](https://www.prijsprofeet.nl/api-account/), under *Bèta*, and
give feedback there too. Currently in beta:

- [Notification after the nightly run](#notification-after-the-nightly-run): one webhook
  per morning as soon as last night's data is in.

### Notification after the nightly run

Want to know when last night's data is in, instead of syncing on a guess? Sign up in your
[API account](https://www.prijsprofeet.nl/api-account/), under *Bèta*, and provide an
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

Available on every plan. On Pro or Business, the checkbox at sign-up accepts the beta
article of version 1.14 of the terms right away: for paid plans that version otherwise
takes effect on 13 November 2026, 30 days after the announcement
([art. 16, in Dutch](https://www.prijsprofeet.nl/api-voorwaarden)).

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
