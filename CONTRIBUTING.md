# Bijdragen

Deze repository bevat de **documentatie** bij de PrijsProfeet-API: de
OpenAPI-specificatie, voorbeeldcode en de changelog. De API zelf en de scrapers
erachter zijn closed source en zitten hier niet in.

## Waar hoort wat

| Wat | Waar |
|---|---|
| Een endpoint doet niet wat de spec zegt | [Issue](../../issues) |
| Data klopt niet (verkeerde prijs, categorie, ontbrekend product) | [Issue](../../issues) |
| Je mist data, een veld of een endpoint | [Issue](../../issues) |
| Fout in de voorbeeldcode of de README | Issue of pull request |
| "Hoe pak ik X aan?" | [Discussions](../../discussions) |
| Vraag over een plan, factuur of de voorwaarden | info@prijsprofeet.nl |
| Storing die *nu* speelt | info@prijsprofeet.nl |

Twee dingen waar we niets mee kunnen, om teleurstelling te voorkomen:

- **"Voeg keten X toe"** — dat kan een prima wens zijn, maar het is een
  scraperbouw van dagen plus permanent onderhoud, dus het gebeurt niet op basis
  van een issue alleen. Vertel liever wát je ermee zou bouwen; dat weegt zwaarder
  dan de wens zelf.
- **Vragen over hoe wij de data verzamelen.** Daar gaan we publiek niet op in.

## Data-issues zijn welkom

Serieus: die zijn nuttig. Foutmeldingen van API-gebruikers hebben de
categorie-indeling en de productvelden al meermaals verbeterd. Geef het
`product_id`, de keten en wat je verwacht had — dan is het na te rekenen.

## Pull requests

Voor de voorbeeldcode: houd het op de standard library, zonder dependencies, zodat
elk voorbeeld met één `python3 examples/...` draait. Voorbeelden die de hele
catalogus binnenhalen nemen we niet op — de limieten zijn er om verkeer te
spreiden, en een voorbeeld hoort niet voor te doen hoe je eromheen werkt.

`openapi.json` wordt gegenereerd uit de draaiende API en is niet met de hand te
bewerken; klopt er iets niet, open dan een issue.
