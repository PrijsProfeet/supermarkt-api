#!/usr/bin/env python3
"""Zoek producten en toon alleen de aanbiedingen die vandaag echt lopen.

Geen key nodig, geen dependencies — alleen de standard library.

    python3 examples/zoeken.py koffie
"""

import json
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://www.prijsprofeet.nl/api/v1"

# Noem jezelf. Zonder key is dit de enige manier waarop we je kunnen bereiken
# bij een breaking change. Zet er geen 'bot'/'crawler'/'spider'/'slurp' in:
# die woorden geven zonder key een 403.
USER_AGENT = "PrijsProfeetVoorbeeld/1.0 (+https://github.com/PrijsProfeet/supermarkt-api)"


def get(path: str, **params) -> dict:
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 429:
            sys.exit("Rate limit geraakt. Zonder key is dat 120/min op zoeken.")
        if error.code == 403:
            sys.exit("403 — zit er 'bot' of 'crawler' in je User-Agent?")
        raise


def main() -> None:
    term = sys.argv[1] if len(sys.argv) > 1 else "koffie"
    data = get("/search", q=term, page_size=25)

    # Een resultaat kan 'upcoming' zijn (begint pas volgende week) of
    # 'historical'. Wie daar niet op filtert toont prijzen die vandaag niet
    # bestaan.
    live = [p for p in data["results"] if p.get("promotion_status") == "active"]

    print(f"{data['total']} treffers voor {term!r}, {len(live)} lopen nu\n")
    for product in sorted(live, key=lambda p: p.get("savings_percentage") or 0, reverse=True):
        was = product.get("original_price")
        korting = f"-{product['savings_percentage']:.0f}%" if product.get("savings_percentage") else ""
        print(
            f"  {product['retailer']:<13} €{product['price']:>6.2f}"
            f"{f' (was €{was:.2f})' if was else '':<16} {korting:<6} {product['name']}"
        )
        if product.get("valid_until"):
            print(f"  {'':<13} t/m {product['valid_until'][:10]}")


if __name__ == "__main__":
    main()
