#!/usr/bin/env python3
"""De twee READMEs moeten dezelfde structuur hebben, en hun eigen ankers raken.

`README.md` is Nederlands en de bron; `README.en.md` is de Engelse kopie. Ze
horen in hetzelfde commit mee te veranderen, en dat controleerde niets: twee keer
in zes dagen kreeg de Nederlandse een stuk dat de Engelse nooit kreeg (`40058ef`
voor `pack_size` en de koffieregel, en de sectie "Datafouten melden", die
helemaal ontbrak). Beide keren viel het op doordat iemand het met het oog zag.

Twee controles, allebei afgeleid uit de bestanden zelf — geen lijst om bij te
houden, want juist een hand-bijgehouden lijst verouderde hier stil:

1. **Pariteit.** Dezelfde koppen op dezelfde plek, met hetzelfde niveau. Gemeten
   2026-11-19 zijn de twee bestanden strikt parallel (19 koppen, identieke
   niveaureeks, één op één), dus een afwijking is per definitie een gat en geen
   stijlkeuze. Beide richtingen tellen: Nederlands is de bron, dus een sectie die
   alleen in het Engels bestaat is net zo goed een fout.
2. **Ankers.** Elke interne link `](#anker)` wijst naar een kop in zijn EIGEN
   bestand. Dat is de andere helft van dezelfde fout: een Engels anker op een
   Nederlandse pagina is geen 404 maar springt niet, dus zo'n link landt stil
   boven de verkeerde tekst.

De ankerregel is die van GitHub en is tegen de echte gerenderde pagina getoetst
(2026-11-19, alle 19 ankers gelijk): kleine letters, alles weg wat geen letter,
cijfer, spatie of koppelteken is, spaties worden koppeltekens. Een kastlijntje
verdwijnt dus en laat twee koppeltekens achter ("what-this-is--and-what-it-isnt").

Alleen de standard library, zoals de voorbeelden in deze repo.
"""

from __future__ import annotations

import pathlib
import re
import sys

NL = "README.md"
EN = "README.en.md"

_KOP = re.compile(r"^(#+) (.+)$")
_INTERNE_LINK = re.compile(r"\]\(#([^)]+)\)")


def anker(kop: str) -> str:
    r"""De id die GitHub van een kop maakt.

    ⚠️ Letters met een accent BLIJVEN staan: de kop "Bèta" wordt `bèta`, niet
    `bta` (gemeten tegen de gerenderde pagina 2026-11-19). Een regex op
    `[a-z0-9]` gooit ze eruit en verzint dan een anker dat niet bestaat — en
    erger, een linkpatroon dat alleen ASCII matcht slaat zo'n link stil OVER,
    waardoor de controle hem nooit ziet. Daarom `\w` met unicode.
    """
    return re.sub(r"[^\w \-]", "", kop.lower(), flags=re.UNICODE).replace(" ", "-")


def koppen(tekst: str) -> list[tuple[int, str]]:
    """(niveau, tekst) per kop, buiten codeblokken.

    Een regel die met `#` begint is binnen een ``` -blok een shell-commentaar en
    geen kop; vandaag staat er geen, maar één `curl`-voorbeeld met commentaar
    erin zou een naïeve parser een kop laten zien die er niet is.
    """
    uit: list[tuple[int, str]] = []
    in_blok = False
    for regel in tekst.splitlines():
        if regel.startswith("```"):
            in_blok = not in_blok
            continue
        if not in_blok and (m := _KOP.match(regel)):
            uit.append((len(m.group(1)), m.group(2).strip()))
    return uit


def controleer_pariteit(nl: list[tuple[int, str]], en: list[tuple[int, str]]) -> list[str]:
    fouten = []
    for i, (a, b) in enumerate(zip(nl, en)):
        if a[0] != b[0]:
            fouten.append(
                f"kop {i + 1} staat op een ander niveau: "
                f"{NL} h{a[0]} {a[1]!r} tegen {EN} h{b[0]} {b[1]!r}"
            )
    for kop in nl[len(en) :]:
        fouten.append(
            f"{EN} mist een sectie die {NL} wel heeft: h{kop[0]} {kop[1]!r}. "
            f"Schrijf de Engelse versie erbij; ze horen in hetzelfde commit mee."
        )
    for kop in en[len(nl) :]:
        fouten.append(
            f"{NL} mist een sectie die {EN} wel heeft: h{kop[0]} {kop[1]!r}. "
            f"Nederlands is de bron, dus die kant hoort er eerst te staan."
        )
    return fouten


def controleer_ankers(naam: str, tekst: str, eigen_koppen: list[tuple[int, str]]) -> list[str]:
    bestaand = {anker(k) for _, k in eigen_koppen}
    return [
        f"{naam} linkt naar #{a}, en dat anker bestaat daar niet. "
        f"Een onbekend anker is geen 404 maar springt niet, dus dit valt stil."
        for a in dict.fromkeys(_INTERNE_LINK.findall(tekst))
        if a not in bestaand
    ]


def main() -> int:
    hier = pathlib.Path(__file__).resolve().parents[2]
    teksten = {}
    for naam in (NL, EN):
        pad = hier / naam
        if not pad.is_file():
            print(f"FOUT: {naam} bestaat niet op {pad}", file=sys.stderr)
            return 1
        teksten[naam] = pad.read_text(encoding="utf-8")

    alle_koppen = {naam: koppen(t) for naam, t in teksten.items()}

    # "Niets gevonden" en "niet gekeken" mogen niet hetzelfde antwoord geven.
    for naam, ks in alle_koppen.items():
        if not ks:
            print(f"FOUT: geen enkele kop gevonden in {naam}; de controle keek niet.", file=sys.stderr)
            return 1

    fouten = controleer_pariteit(alle_koppen[NL], alle_koppen[EN])
    for naam in (NL, EN):
        fouten += controleer_ankers(naam, teksten[naam], alle_koppen[naam])

    if fouten:
        print(f"De twee READMEs lopen uiteen ({len(fouten)}):", file=sys.stderr)
        for f in fouten:
            print(f"  - {f}", file=sys.stderr)
        return 1

    print(
        f"OK: {len(alle_koppen[NL])} koppen in beide READMEs, zelfde structuur, "
        f"alle interne ankers bestaan."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
