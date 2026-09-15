#!/usr/bin/env python3
"""Controleert de dataset in index.html.

Draai dit voordat je commit. Faalt als de app iets zou tonen dat niet uit de
onderliggende feedback komt, of als er een export in de repo is beland.

    python3 controle.py
"""

import json
import pathlib
import re
import sys

WORTEL = pathlib.Path(__file__).parent
fouten = []


def lees_data():
    html = (WORTEL / "index.html").read_text(encoding="utf-8")
    blok = re.search(
        r'<script id="feedforward-data" type="application/json">(.*?)</script>',
        html,
        re.S,
    )
    if not blok:
        sys.exit("FOUT: het datablok staat niet in index.html")
    return json.loads(blok.group(1))


def controleer(data):
    per_id = {}
    for f in data["feedback"]:
        if f["id"] in per_id:
            fouten.append(f"dubbel feedback-id: {f['id']}")
        per_id[f["id"]] = f

    pagina_ids = {p["id"] for p in data["paginas"]}
    for f in data["feedback"]:
        if f["pagina"] not in pagina_ids:
            fouten.append(f"{f['id']} verwijst naar onbekende pagina {f['pagina']}")
        if not f["tekst"].strip():
            fouten.append(f"{f['id']} heeft geen tekst")

    for p in data["paginas"]:
        items = [f for f in data["feedback"] if f["pagina"] == p["id"]]
        if not items:
            fouten.append(f"{p['id']}: geen feedback")
        if not 2 <= len(p["oorzaken"]) <= 4:
            fouten.append(f"{p['id']}: {len(p['oorzaken'])} oorzaken (moet 2 t/m 4 zijn)")
        for o in p["oorzaken"]:
            if len(o["citaat_ids"]) < 2:
                fouten.append(f"{p['id']} / '{o['titel']}': minder dan 2 citaten")
            if not o["suggesties"]:
                fouten.append(f"{p['id']} / '{o['titel']}': geen suggesties")
            for cid in o["citaat_ids"]:
                if cid not in per_id:
                    fouten.append(f"{p['id']}: citaat {cid} bestaat niet in de feedback")
                elif per_id[cid]["pagina"] != p["id"]:
                    fouten.append(f"{p['id']}: citaat {cid} hoort bij een andere pagina")
    return per_id


def controleer_privacy(data):
    """Bij echte data mag er geen persoonsgegeven in de citaten staan."""
    patronen = {
        "e-mailadres": r"[\w.+-]+@[\w-]+\.[\w.]+",
        "telefoonnummer": r"\+?\d[\d\s-]{8,}\d",
        "postcode": r"\b\d{4}\s?[A-Za-z]{2}\b",
    }
    for f in data["feedback"]:
        for naam, patroon in patronen.items():
            if re.search(patroon, f["tekst"]):
                fouten.append(f"{f['id']}: lijkt een {naam} te bevatten")


def controleer_repo():
    for pad in WORTEL.rglob("*"):
        if pad.suffix.lower() in {".csv", ".xlsx", ".xls", ".tsv"}:
            fouten.append(f"export in de repo: {pad.relative_to(WORTEL)}")


def main():
    data = lees_data()
    per_id = controleer(data)
    controleer_privacy(data)
    controleer_repo()

    if data["meta"].get("is_voorbeelddata"):
        print("LET OP: dit is voorbeelddata, geen echte bezoekersfeedback.")

    gebruikt = {c for p in data["paginas"] for o in p["oorzaken"] for c in o["citaat_ids"]}
    print(
        f"{len(data['paginas'])} pagina's, {len(per_id)} feedbackitems, "
        f"{len(gebruikt)} daarvan als citaat getoond."
    )

    if fouten:
        print(f"\n{len(fouten)} fout(en):")
        for f in fouten:
            print("  -", f)
        sys.exit(1)
    print("Alle controles geslaagd.")


if __name__ == "__main__":
    main()
