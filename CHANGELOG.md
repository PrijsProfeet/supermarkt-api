# Changelog

**Het volledige overzicht staat op [prijsprofeet.nl/api](https://www.prijsprofeet.nl/api#wat-is-nieuw)** —
met per wijziging wat er precies veranderde en wat het voor je integratie betekent.
Dat is de canonieke versie; hier staan korte regels die ernaar verwijzen, zodat de
twee niet uit elkaar kunnen lopen.

Elke wijziging krijgt hier een **GitHub Release**. Zet de repo op *Watch → Releases*
als je bericht wilt krijgen zonder een pagina in de gaten te houden.

Nieuwe velden, nieuwe ketens en betere dekking rollen we zonder aankondiging uit.
**Breaking changes op een betaald endpoint kondigen we minimaal 30 dagen van tevoren
aan** (art. 10 van de [API-voorwaarden](https://www.prijsprofeet.nl/api-voorwaarden)):
per e-mail aan betalende afnemers én hier.

## 2026-08-09

- **De OpenAPI-specificatie is nu machinaal op te halen.** Tot nu toe was de spec
  alleen in een browser te bekijken op [/docs](https://www.prijsprofeet.nl/docs);
  geautomatiseerde clients krijgen daar een `403`, dus codegeneratie was onmogelijk.
  [`openapi.json`](openapi.json) in deze repo is de kopie die je wél kunt ophalen.
  Geen wijziging aan de API zelf.
