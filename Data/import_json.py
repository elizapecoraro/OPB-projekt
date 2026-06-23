"""Uvoz oziroma posodobitev podatkov OSM v PostgreSQL."""

import json
import re
from pathlib import Path

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
        """
        INSERT INTO lokacija (ime_lokacije)
        VALUES (%s)
        ON CONFLICT (ime_lokacije)
        DO UPDATE SET ime_lokacije = EXCLUDED.ime_lokacije
        RETURNING lokacija_id
        """,
        [ime_lokacije],
    )
    return cur.fetchone()["lokacija_id"]


def get_or_create_kuhinja(cur, vrsta):
    cur.execute(
        """
        INSERT INTO kuhinja (vrsta)
        VALUES (%s)
        ON CONFLICT (vrsta)
        DO UPDATE SET vrsta = EXCLUDED.vrsta
        RETURNING kuhinja_id
        """,
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


def razcleni_cas(cas):
    """
    Razčleni tudi razširjene OSM-ure, na primer 28:00.

    28:00 pomeni 04:00 naslednji dan, zato funkcija vrne:
    - zamik dneva,
    - običajno uro,
    - število minut v običajnem dnevu.
    """
    zadetek = re.fullmatch(r"(\d{1,2}):([0-5]\d)", cas.strip())

    if not zadetek:
        return None

    ura = int(zadetek.group(1))
    minuta = int(zadetek.group(2))

    zamik_dneva = ura // 24
    ura_v_dnevu = ura % 24
    normaliziran_cas = f"{ura_v_dnevu:02d}:{minuta:02d}"
    minute_v_dnevu = ura_v_dnevu * 60 + minuta

    return zamik_dneva, normaliziran_cas, minute_v_dnevu


def premakni_dan(dan, zamik):
    """Premakne dan v tednu; 1 je ponedeljek, 7 je nedelja."""
    return ((dan - 1 + zamik) % 7) + 1


def dodaj_interval(vrstice, dan, ura_od_raw, ura_do_raw):
    """
    Interval, ki gre čez polnoč, razdeli na več vrstic.

    Primer:
    petek 08:00-28:00

    postane:
    petek 08:00-23:59:59
    sobota 00:00-04:00
    """
    zacetek = razcleni_cas(ura_od_raw)
    konec = razcleni_cas(ura_do_raw)

    if not zacetek or not konec:
        return

    zacetni_zamik, ura_od, minute_od = zacetek
    koncni_zamik, ura_do, minute_do = konec

    # Tudi zapis 18:00-02:00 pomeni, da se interval konča naslednji dan.
    if koncni_zamik == zacetni_zamik and minute_do <= minute_od:
        koncni_zamik += 1

    if koncni_zamik < zacetni_zamik:
        return

    # Interval se konča isti dan.
    if zacetni_zamik == koncni_zamik:
        vrstice.append(
            (
                premakni_dan(dan, zacetni_zamik),
                ura_od,
                ura_do,
            )
        )
        return

    # Prvi del intervala: od začetne ure do konca dneva.
    vrstice.append(
        (
            premakni_dan(dan, zacetni_zamik),
            ura_od,
            "23:59:59",
        )
    )

    # Morebitni polni dnevi med začetkom in koncem.
    for zamik in range(zacetni_zamik + 1, koncni_zamik):
        vrstice.append(
            (
                premakni_dan(dan, zamik),
                "00:00",
                "23:59:59",
            )
        )

    # Če se interval ne konča natančno ob polnoči, dodamo še zadnji del.
    if ura_do != "00:00":
        vrstice.append(
            (
                premakni_dan(dan, koncni_zamik),
                "00:00",
                ura_do,
            )
        )


def razsiri_dneve(izraz):
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
                dnevi = DNEVI_ORDER[i : j + 1]
            else:
                dnevi = DNEVI_ORDER[i:] + DNEVI_ORDER[: j + 1]

            rezultat.extend(DNEVI[d] for d in dnevi)
        elif del_izraza in DNEVI:
            rezultat.append(DNEVI[del_izraza])

    return rezultat


def parse_opening_hours(opening_hours):
    """Razčleni pogoste zapise delovnega časa iz OpenStreetMap."""

    if not opening_hours:
        return []

    if opening_hours.strip() == "24/7":
        return [
            (dan, "00:00", "23:59:59")
            for dan in range(1, 8)
        ]

    vrstice = []

    for pravilo in opening_hours.split(";"):
        pravilo = pravilo.strip()

        if not pravilo or "off" in pravilo.lower():
            continue

        deli = pravilo.split(maxsplit=1)

        if len(deli) < 2:
            continue

        dnevi_del, ure_del = deli
        dnevi = razsiri_dneve(dnevi_del)

        for interval in ure_del.split(","):
            interval = interval.strip()

            if "-" not in interval:
                continue

            ura_od, ura_do = interval.split("-", 1)

            for dan in dnevi:
                dodaj_interval(
                    vrstice,
                    dan,
                    ura_od.strip(),
                    ura_do.strip(),
                )

    return vrstice

def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Datoteka {DATA_PATH} ne obstaja. Najprej zaženi "
            "'python -m Data.download_osm'."
        )

    with DATA_PATH.open(encoding="utf-8") as datoteka:
        data = json.load(datoteka)

    elementi = data.get("elements")
    if not isinstance(elementi, list):
        raise ValueError("JSON ne vsebuje veljavnega seznama 'elements'.")

    obdelanih = 0

    with get_cursor() as cur:
        for element in elementi:
            tags = element.get("tags", {})
            ime = tags.get("name")
            if not ime:
                continue

            osm_id = element.get("id")
            osm_tip = element.get("type")
            if osm_id is None or not osm_tip:
                continue

            center = element.get("center", {})
            lat = element.get("lat") or center.get("lat")
            lon = element.get("lon") or center.get("lon")
            opening_hours = tags.get("opening_hours")

            ime_lokacije = (
                tags.get("addr:city")
                or tags.get("addr:town")
                or tags.get("addr:village")
                or tags.get("addr:municipality")
                or "Neznano"
            )
            lokacija_id = get_or_create_lokacija(
                cur, normaliziraj_lokacijo(ime_lokacije)
            )

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
                ON CONFLICT (osm_id, osm_tip)
                DO UPDATE SET
                    ime = EXCLUDED.ime,
                    ulica = EXCLUDED.ulica,
                    hisna_stevilka = EXCLUDED.hisna_stevilka,
                    telefon = EXCLUDED.telefon,
                    spletna_stran = EXCLUDED.spletna_stran,
                    zemljepisna_sirina = EXCLUDED.zemljepisna_sirina,
                    zemljepisna_dolzina = EXCLUDED.zemljepisna_dolzina,
                    opening_hours_raw = EXCLUDED.opening_hours_raw,
                    lokacija_id = EXCLUDED.lokacija_id
                RETURNING restavracija_id
                """,
                [
                    osm_id,
                    osm_tip,
                    ime,
                    tags.get("addr:street"),
                    tags.get("addr:housenumber"),
                    tags.get("phone") or tags.get("contact:phone"),
                    tags.get("website") or tags.get("contact:website"),
                    lat,
                    lon,
                    opening_hours,
                    lokacija_id,
                ],
            )
            restavracija_id = cur.fetchone()["restavracija_id"]

            # Povezani podatki se na novo ustvarijo, da se posodobijo tudi
            # spremenjene ali odstranjene kuhinje in ure.
            cur.execute(
                "DELETE FROM delovni_cas WHERE restavracija_id = %s",
                [restavracija_id],
            )
            cur.execute(
                "DELETE FROM restavracija_kuhinja WHERE restavracija_id = %s",
                [restavracija_id],
            )

            for dan, ura_od, ura_do in parse_opening_hours(opening_hours):
                cur.execute(
                    """
                    INSERT INTO delovni_cas (
                        restavracija_id, dan_v_tednu, ura_od, ura_do
                    )
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
                        INSERT INTO restavracija_kuhinja (
                            restavracija_id, kuhinja_id
                        )
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING
                        """,
                        [restavracija_id, kuhinja_id],
                    )

            obdelanih += 1

    print(f"Uvoženih ali posodobljenih restavracij: {obdelanih}")


if __name__ == "__main__":
    main()
