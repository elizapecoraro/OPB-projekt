import json
from pathlib import Path

from Data.database import get_cursor


DATA_PATH = Path(__file__).with_name("restavracije_slovenija.json")


def get_or_create_lokacija(cur, ime_lokacije):
    cur.execute(
        "SELECT lokacija_id FROM lokacija WHERE ime_lokacije = %s",
        [ime_lokacije],
    )
    row = cur.fetchone()

    if row:
        return row["lokacija_id"]

    cur.execute(
        "INSERT INTO lokacija (ime_lokacije) VALUES (%s) RETURNING lokacija_id",
        [ime_lokacije],
    )
    return cur.fetchone()["lokacija_id"]


def get_or_create_kuhinja(cur, vrsta):
    cur.execute(
        "SELECT kuhinja_id FROM kuhinja WHERE vrsta = %s",
        [vrsta],
    )
    row = cur.fetchone()

    if row:
        return row["kuhinja_id"]

    cur.execute(
        "INSERT INTO kuhinja (vrsta) VALUES (%s) RETURNING kuhinja_id",
        [vrsta],
    )
    return cur.fetchone()["kuhinja_id"]


def main():
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)

    dodanih = 0

    with get_cursor() as cur:
        for el in data.get("elements", []):
            tags = el.get("tags", {})
            ime = tags.get("name")

            if not ime:
                continue

            osm_id = el.get("id")
            osm_tip = el.get("type")

            # Da ne uvoziš iste restavracije večkrat
            cur.execute(
                """
                SELECT restavracija_id
                FROM restavracija
                WHERE osm_id = %s AND osm_tip = %s
                """,
                [osm_id, osm_tip],
            )
            if cur.fetchone():
                continue

            center = el.get("center", {})
            lat = el.get("lat") or center.get("lat")
            lon = el.get("lon") or center.get("lon")

            ime_lokacije = (
                tags.get("addr:city")
                or tags.get("addr:town")
                or tags.get("addr:village")
                or tags.get("addr:municipality")
                or "Neznano"
            )

            lokacija_id = get_or_create_lokacija(cur, ime_lokacije)

            cur.execute(
                """
                INSERT INTO restavracija (
                    osm_id,
                    osm_tip,
                    ime,
                    ulica,
                    hisna_stevilka,
                    telefon,
                    spletna_stran,
                    zemljepisna_sirina,
                    zemljepisna_dolzina,
                    lokacija_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING restavracija_id
                """,
                [
                    osm_id,
                    osm_tip,
                    ime,
                    tags.get("addr:street"),
                    tags.get("addr:housenumber"),
                    tags.get("phone"),
                    tags.get("website"),
                    lat,
                    lon,
                    lokacija_id,
                ],
            )

            restavracija_id = cur.fetchone()["restavracija_id"]

            cuisine = tags.get("cuisine")
            if cuisine:
                for vrsta in cuisine.split(";"):
                    vrsta = vrsta.strip()
                    if not vrsta:
                        continue

                    kuhinja_id = get_or_create_kuhinja(cur, vrsta)

                    cur.execute(
                        """
                        INSERT INTO restavracija_kuhinja (restavracija_id, kuhinja_id)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING
                        """,
                        [restavracija_id, kuhinja_id],
                    )

            dodanih += 1

    print(f"Uvoženih restavracij: {dodanih}")


if __name__ == "__main__":
    main()