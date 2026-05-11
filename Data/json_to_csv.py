import json
import csv

# odpri JSON
with open("restavracije_slovenija.json", "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []

for el in data["elements"]:

    tags = el.get("tags", {})

    # koordinate
    lat = el.get("lat")
    lon = el.get("lon")

    # pri way/relation uporabimo center
    if lat is None or lon is None:
        center = el.get("center", {})
        lat = center.get("lat")
        lon = center.get("lon")

    row = {
        "osm_id": el.get("id"),
        "osm_tip": el.get("type"),
        "ime": tags.get("name"),
        "ulica": tags.get("addr:street"),
        "hisna_stevilka": tags.get("addr:housenumber"),
        "mesto": tags.get("addr:city"),
        "telefon": tags.get("phone"),
        "spletna_stran": tags.get("website"),
        "cuisine": tags.get("cuisine"),
        "zemljepisna_sirina": lat,
        "zemljepisna_dolzina": lon
    }

    # obdrži samo restavracije z imenom
    if row["ime"]:
        rows.append(row)

# shrani CSV
with open("restavracije.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Izvoženih {len(rows)} restavracij.")