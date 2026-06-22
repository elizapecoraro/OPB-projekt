import json
from pathlib import Path
import re

from Data.database import get_cursor


DATA_PATH = Path(__file__).with_name("restavracije_slovenija.json")

def normaliziraj_lokacijo(ime_lokacije):
    if not ime_lokacije:
        return "Neznano"

    ime = ime_lokacije.strip()

    popravki = {
        "Ajdovscina": "Ajdovščina",
        "Bohinjsko Jezero": "Bohinjsko jezero",
        "Jesenice na dolenjskem": "Jesenice na Dolenjskem",
        "kostanjevica": "Kostanjevica",
        "Nova vas": "Nova Vas",
        "velike Lašče": "Velike Lašče",
        "Ljubjana": "Ljubljana",
        "Ljublijana": "Ljubljana",
        "Ljubljana-Dobrunje": "Ljubljana - Dobrunje",
        "Koper - Capodistria": "Koper",
        "Koper / Capodistria": "Koper",
        "Koper-Capodistria": "Koper",
        "Izola - Isola": "Izola",
        "Izola / Isola": "Izola",
        "Piran - Pirano": "Piran",
        "Portorož - Portorose": "Portorož",
        "Ratece - Planica": "Rateče - Planica",
        "Šmarje-Sap": "Šmarje - Sap",
        "Sv. Trojica v Slov. goricah": "Sv. Trojica v Slovenskih goricah",
        "Lenart v Slov. goricah": "Lenart v Slovenskih Goricah",
    }

    return popravki.get(ime, ime)


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

DNEVI = {
    "Mo": 1,
    "Tu": 2,
    "We": 3,
    "Th": 4,
    "Fr": 5,
    "Sa": 6,
    "Su": 7,
}

DNEVI_ORDER = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]


def normaliziraj_cas(cas):
    """
    Vrne čas v obliki HH:MM ali None.
    Primer: "9:00" -> "09:00"
    """
    cas = cas.strip()

    if re.match(r"^\d:\d{2}$", cas):
        return "0" + cas

    if re.match(r"^\d{2}:\d{2}$", cas):
        return cas

    return None


def razsiri_dneve(izraz):
    """
    Primeri:
    "Mo" -> [1]
    "Mo-Fr" -> [1, 2, 3, 4, 5]
    "Sa,Su" -> [6, 7]
    """
    rezultat = []

    for del_izraza in izraz.split(","):
        del_izraza = del_izraza.strip()

        if "-" in del_izraza:
            zacetek, konec = del_izraza.split("-", 1)
            zacetek = zacetek.strip()
            konec = konec.strip()

            if zacetek not in DNEVI or konec not in DNEVI:
                continue

            i = DNEVI_ORDER.index(zacetek)
            j = DNEVI_ORDER.index(konec)

            if i <= j:
                dnevi = DNEVI_ORDER[i:j + 1]
            else:
                dnevi = DNEVI_ORDER[i:] + DNEVI_ORDER[:j + 1]

            rezultat.extend(DNEVI[d] for d in dnevi)

        else:
            if del_izraza in DNEVI:
                rezultat.append(DNEVI[del_izraza])

    return rezultat


def parse_opening_hours(opening_hours):
    """
    Preprost parser za pogoste OSM oblike:
    - Mo-Fr 10:00-22:00
    - Mo-Fr 10:00-22:00; Sa 12:00-23:00; Su 12:00-21:00
    - Sa,Su 12:00-22:00

    Kompleksne zapise, kot so "PH off", "sunrise-sunset" ali več pravil na isti dan,
    zaenkrat preskočimo. To je za projekt čisto dovolj kot prvi delujoč korak.
    """
    if not opening_hours:
        return []

    vrstice = []

    for pravilo in opening_hours.split(";"):
        pravilo = pravilo.strip()

        if not pravilo:
            continue

        if "off" in pravilo.lower():
            continue

        deli = pravilo.split()

        if len(deli) < 2:
            continue

        dnevi_del = deli[0]
        ure_del = deli[1]

        dnevi = razsiri_dneve(dnevi_del)

        for interval in ure_del.split(","):
            if "-" not in interval:
                continue

            ura_od, ura_do = interval.split("-", 1)
            ura_od = normaliziraj_cas(ura_od)
            ura_do = normaliziraj_cas(ura_do)

            if not ura_od or not ura_do:
                continue

            for dan in dnevi:
                vrstice.append((dan, ura_od, ura_do))

    return vrstice


def main():
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)

    dodanih = 0

    with get_cursor() as cur:
        for el in data.get("elements", []):
            tags = el.get("tags", {})
            opening_hours = tags.get("opening_hours")

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

            ime_lokacije = normaliziraj_lokacijo(ime_lokacije)
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
                    opening_hours_raw,
                    lokacija_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                    opening_hours,
                    lokacija_id,
                ],
            )

            restavracija_id = cur.fetchone()["restavracija_id"]

            for dan, ura_od, ura_do in parse_opening_hours(opening_hours):
                cur.execute(
                    """
                    INSERT INTO delovni_cas (restavracija_id, dan_v_tednu, ura_od, ura_do)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    [restavracija_id, dan, ura_od, ura_do],
                )

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