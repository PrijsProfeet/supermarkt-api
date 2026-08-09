#!/usr/bin/env python3
"""Zoek een product en haal het volledige detail op.

Laat en passant zien waarom je op de EAN wilt koppelen als die er is: bij
Albert Heijn, Jumbo, Dirk en DekaMarkt is hij er vrijwel altijd, bij Aldi,
Lidl, Hoogvliet en Vomar publiceert de keten er geen.

    python3 examples/product_detail.py "pindakaas"
"""

import json
import sys
import urllib.parse
import urllib.request

BASE = "https://www.prijsprofeet.nl/api/v1"
USER_AGENT = "PrijsProfeetVoorbeeld/1.0 (+https://github.com/PrijsProfeet/supermarkt-api)"


def get(path: str, **params) -> dict:
    url = f"{BASE}{path}" + (f"?{urllib.parse.urlencode(params)}" if params else "")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.load(response)


def main() -> None:
    term = sys.argv[1] if len(sys.argv) > 1 else "pindakaas"

    treffers = get("/search", q=term, page_size=1)["results"]
    if not treffers:
        sys.exit(f"Niets gevonden voor {term!r}")

    # Let op: product_id bevat de promotieweek en verandert dus per week.
    # Wil je een product over weken heen volgen, bewaar dan base_product_id.
    product = get(f"/products/{treffers[0]['product_id']}")

    print(f"{product['name']}  —  {product['retailer']}")
    print(f"  merk         {product.get('brand') or '—'}")
    print(f"  prijs        €{product['price']:.2f}", end="")
    if product.get("original_price"):
        print(f"  (was €{product['original_price']:.2f}, -{product.get('discount_percentage') or 0:.0f}%)")
    else:
        print()
    print(f"  inhoud       {product.get('quantity') or '—'}  ({product.get('unit_price') or '—'})")
    print(f"  categorie    {product.get('unified_category') or '—'}")
    print(f"  dieet        {', '.join(product.get('dietary_tags') or []) or '—'}")
    print(f"  EAN          {product.get('ean') or '— (deze keten publiceert er geen)'}")
    print(f"  huismerk     {'ja' if product.get('private_label') else 'nee'}")
    print(f"  bij de keten {product.get('product_url') or '—'}")


if __name__ == "__main__":
    main()
