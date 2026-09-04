#!/usr/bin/env python3
"""Zoek een product en vergelijk het op EAN bij de andere ketens.

`/match/*` zit achter een betaald plan. Zet je key in de omgeving:

    export PRIJSPROFEET_API_KEY=...
    python3 examples/matching.py "doritos"

Waar dit voorbeeld voor bestaat: in `openapi.json` staat de respons van
`/match/*` als een ongetypeerd object, dus de parameters zijn daar volledig
beschreven en de veldnamen niet. Hieronder staan ze wel, en met opzet ook de
valkuil — `min(price)` over alle matches geeft een prijs die vandaag niet te
koop hoeft te zijn.
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://www.prijsprofeet.nl/api/v1"
USER_AGENT = "PrijsProfeetVoorbeeld/1.0 (+https://github.com/PrijsProfeet/supermarkt-api)"

# De vier waarden van promotion_status. Dit veld beslist of een prijs vandaag
# betaalbaar is; alleen `active` is dat met zekerheid.
STATUS = {
    "active": "loopt nu",
    "upcoming": "begint volgende week",
    "shelf": "reguliere prijs van vandaag",
    "historical": "laatst door ons gezien (max 60 dagen terug)",
}


def get(path: str, **params) -> dict:
    url = f"{BASE}{path}" + (f"?{urllib.parse.urlencode(params)}" if params else "")
    headers = {"User-Agent": USER_AGENT}
    key = os.environ.get("PRIJSPROFEET_API_KEY")
    if key:
        headers["X-API-Key"] = key
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.load(response)


def main() -> None:
    term = sys.argv[1] if len(sys.argv) > 1 else "doritos"

    # Zoeken kan zonder key; matchen niet.
    treffers = [r for r in get("/search", q=term, page_size=20)["results"] if r.get("ean")]
    if not treffers:
        sys.exit(f"Geen treffer met een EAN voor {term!r} — vier ketens publiceren er geen.")
    bron = treffers[0]

    try:
        antwoord = get(f"/match/ean/{bron['ean']}", exclude_retailer=bron["retailer"])
    except urllib.error.HTTPError as fout:
        # 401 = geen key meegestuurd, 403 = wel een key maar geen betaald plan.
        if fout.code == 401:
            sys.exit("401 — /match/* vraagt een key. Zet PRIJSPROFEET_API_KEY.")
        if fout.code == 403:
            sys.exit("403 — key onbekend, ingetrokken of zonder betaald plan; /match/* zit op Pro.")
        raise

    print(f"{bron['name']}  —  {bron['retailer']}  €{bron['price']:.2f}  (EAN {bron['ean']})")
    print(f"{antwoord['total_matches']} match(es) elders, gesorteerd op prijs:\n")

    for m in antwoord["matches"]:
        status = m.get("promotion_status")
        regel = f"  €{m['price']:.2f}  {m['retailer_display']:<15} {m['name'][:44]:<44}"
        print(f"{regel}  {STATUS.get(status, status or '—')}")
        if m.get("original_price"):
            print(f"      van €{m['original_price']:.2f}, -{m['savings_percentage']}%", end="")
            print(f"  t/m {m['valid_until']}" if m.get("valid_until") else "")
        if m.get("last_deal_price"):
            # De keten stond hier laatst in de actie: die prijs is voorbij, maar
            # zonder deze regel lijkt de winkel duurder dan hij ooit was.
            print(f"      was €{m['last_deal_price']:.2f} in de actie t/m {m['last_deal_until']}")
        if m.get("quantity"):
            print(f"      inhoud {m['quantity']}  ({m.get('unit_price') or '—'})")
        if m.get("price_changed_at"):
            # Alleen op een shelf-rij: sinds wanneer deze reguliere prijs geldt.
            # Spiegel je schapprijzen, dan is dit het veld om op over te slaan.
            print(f"      deze prijs sinds {m['price_changed_at']}")
        if m["match_level"] != "exact_ean":
            print(f"      ≈ vergelijkbaar ({m['match_level']}, zekerheid {m['confidence']})")

    # De valkuil, en de manier eromheen.
    if antwoord["matches"]:
        goedkoopste = min(antwoord["matches"], key=lambda m: m["price"])
        vandaag = [m for m in antwoord["matches"] if m["is_current_deal"]]
        print(f"\n  min(price)          €{goedkoopste['price']:.2f} bij {goedkoopste['retailer_display']}"
              f"  — {STATUS.get(goedkoopste['promotion_status'], '—')}")
        if vandaag:
            beste = min(vandaag, key=lambda m: m["price"])
            print(f"  vandaag te koop     €{beste['price']:.2f} bij {beste['retailer_display']}")
        else:
            print("  vandaag te koop     geen enkele — dit is wat ?current_only=true eruit filtert")


if __name__ == "__main__":
    main()
