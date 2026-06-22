import json
from pathlib import Path

import requests


DATA_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = DATA_DIR / "restavracije_slovenija.json"

OVERPASS_URL = "https://overpass.kumi.systems/api/interpreter"


QUERY = """
[out:json][timeout:180];

(
  node["amenity"~"restaurant|fast_food|cafe"](45.3,13.3,46.9,16.7);
  way["amenity"~"restaurant|fast_food|cafe"](45.3,13.3,46.9,16.7);
  relation["amenity"~"restaurant|fast_food|cafe"](45.3,13.3,46.9,16.7);
);

out center tags;
"""


def prenesi_osm_podatke():
    response = requests.post(
        OVERPASS_URL,
        data={"data": QUERY},
        timeout=240,
    )
    
    response.raise_for_status()
    return response.json()


def main():
    data = prenesi_osm_podatke()

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Podatki so shranjeni v: {OUTPUT_PATH}")
    print(f"Število elementov: {len(data.get('elements', []))}")


if __name__ == "__main__":
    main()