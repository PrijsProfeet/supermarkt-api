#!/usr/bin/env python3
"""Toon de scherpste aanbiedingen van één keten.

/deals/top groepeert per merk: één regel per merkactie, met een
'representative_product' als voorbeeld en 'variant_count' voor het aantal
varianten dat eronder valt.

    python3 examples/aanbiedingen_per_keten.py jumbo
"""

import json
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://www.prijsprofeet.nl/api/v1"
USER_AGENT = "PrijsProfeetVoorbeeld/1.0 (+https://github.com/PrijsProfeet/supermarkt-api)"

# De API accepteert zowel 'albert-heijn' als 'albert_heijn' en geeft 400 op een
# onbekende waarde — een typefout mag nooit lezen als "geen aanbiedingen".
KETENS = (
    "albert_heijn aldi dekamarkt dirk ekoplaza hoogvliet jumbo lidl plus vomar"
).split()


def get(path: str, **params) -> dict:
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 400:
            sys.exit(f"Onbekende keten. Kies uit: {', '.join(KETENS)}")
        if error.code == 429:
            sys.exit("Rate limit geraakt. Zonder key is dat 30/min op dit endpoint.")
        raise


def main() -> None:
    keten = sys.argv[1] if len(sys.argv) > 1 else "jumbo"
    data = get("/deals/top", retailer=keten, limit=10)

    for titel, sleutel in (("Grootste korting %", "top_by_percentage"), ("Grootste besparing €", "top_by_amount")):
        print(f"\n{titel} — {keten}")
        for deal in data.get(sleutel, []):
            product = deal.get("representative_product") or {}
            varianten = deal.get("variant_count") or 1
            print(
                f"  {deal.get('brand') or '?':<22}"
                f" -{deal.get('savings_percentage') or 0:>5.0f}%"
                f"  €{deal.get('savings_amount') or 0:>5.2f} korting"
                f"  {product.get('name', '')[:46]}"
                + (f"  (+{varianten - 1} varianten)" if varianten > 1 else "")
            )


if __name__ == "__main__":
    main()
