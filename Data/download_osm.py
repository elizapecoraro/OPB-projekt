"""Prenos aktualnih podatkov iz OpenStreetMap prek Overpass API."""

import json
from pathlib import Path
from typing import Any

import requests


DATA_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = DATA_DIR / "restavracije_slovenija.json"
OVERPASS_URL = "https://overpass.kumi.systems/api/interpreter"

# Območje je izbrano po državni meji Slovenije, ne po približnem pravokotniku.
# Trenutno zajamemo restavracije, hitro prehrano in kavarne, kot jih je zajemala
# tudi prvotna različica projekta.
QUERY = """
[out:json][timeout:180];

area["ISO3166-1"="SI"][admin_level=2]->.slovenija;

nwr
  ["amenity"~"^(restaurant|fast_food|cafe)$"]
  ["name"]
  (area.slovenija);

out center tags;
"""


def prenesi_osm_podatke() -> dict[str, Any]:
    response = requests.post(
        OVERPASS_URL,
        data={"data": QUERY},
        headers={"User-Agent": "OPB-projekt-restavracije/1.0"},
        timeout=240,
    )
    response.raise_for_status()

    data = response.json()
    elementi = data.get("elements")
    if not isinstance(elementi, list):
        raise ValueError("Overpass API ni vrnil veljavnega seznama 'elements'.")

    return data


def shrani_osm_podatke(data: dict[str, Any]) -> None:
    """Podatke najprej zapiše v začasno datoteko in šele nato zamenja star JSON."""

    zacasna_pot = OUTPUT_PATH.with_suffix(".json.tmp")
    with zacasna_pot.open("w", encoding="utf-8") as datoteka:
        json.dump(data, datoteka, ensure_ascii=False, indent=2)

    zacasna_pot.replace(OUTPUT_PATH)


def main() -> None:
    data = prenesi_osm_podatke()
    shrani_osm_podatke(data)

    print(f"Podatki so shranjeni v: {OUTPUT_PATH}")
    print(f"Število elementov: {len(data['elements'])}")


if __name__ == "__main__":
    main()
