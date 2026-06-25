"""Repozitorij za branje podatkov o restavracijah."""

from Data.database import get_cursor
from Data.models import DelovniCas, Kuhinja, Lokacija, RestavracijaDto


class RestavracijaRepository:
    def seznam_restavracij(
        self,
        iskanje: str | None = None,
        lokacija_id: int | None = None,
        kuhinja_id: int | None = None,
        dan_v_tednu: int | None = None,
        ima_telefon: bool = False,
        ima_spletno_stran: bool = False,
        ima_delovni_cas: bool = False,
        limit: int = 20,
        offset: int = 0,
    ) -> list[RestavracijaDto]:
        query = """
            SELECT
                r.restavracija_id,
                r.ime,
                r.ulica,
                r.hisna_stevilka,
                r.telefon,
                r.spletna_stran,
                r.zemljepisna_sirina,
                r.zemljepisna_dolzina,
                r.opening_hours_raw,
                l.ime_lokacije,
                COALESCE(
                    STRING_AGG(DISTINCT k.vrsta, ', ' ORDER BY k.vrsta),
                    ''
                ) AS kuhinje
            FROM restavracija r
            JOIN lokacija l ON l.lokacija_id = r.lokacija_id
            LEFT JOIN restavracija_kuhinja rk
                ON rk.restavracija_id = r.restavracija_id
            LEFT JOIN kuhinja k ON k.kuhinja_id = rk.kuhinja_id
        """

        where = []
        params = []

        if iskanje:
            where.append(
                """
                (
                    LOWER(r.ime) LIKE LOWER(%s)
                    OR LOWER(l.ime_lokacije) LIKE LOWER(%s)
                    OR LOWER(k.vrsta) LIKE LOWER(%s)
                )
                """
            )
            vzorec = f"%{iskanje}%"
            params.extend([vzorec, vzorec, vzorec])

        if lokacija_id:
            where.append("r.lokacija_id = %s")
            params.append(lokacija_id)

        if kuhinja_id:
            where.append(
                """
                EXISTS (
                    SELECT 1
                    FROM restavracija_kuhinja rk2
                    WHERE rk2.restavracija_id = r.restavracija_id
                      AND rk2.kuhinja_id = %s
                )
                """
            )
            params.append(kuhinja_id)

        if dan_v_tednu:
            where.append(
                """
                EXISTS (
                    SELECT 1
                    FROM delovni_cas dc
                    WHERE dc.restavracija_id = r.restavracija_id
                      AND dc.dan_v_tednu = %s
                )
                """
            )
            params.append(dan_v_tednu)

        if ima_telefon:
            where.append("r.telefon IS NOT NULL AND TRIM(r.telefon) <> ''")

        if ima_spletno_stran:
            where.append(
                "r.spletna_stran IS NOT NULL AND TRIM(r.spletna_stran) <> ''"
            )

        if ima_delovni_cas:
            where.append(
                """
                EXISTS (
                    SELECT 1
                    FROM delovni_cas dc2
                    WHERE dc2.restavracija_id = r.restavracija_id
                )
                """
            )

        if where:
            query += " WHERE " + " AND ".join(where)

        query += """
            GROUP BY r.restavracija_id, l.ime_lokacije
            ORDER BY r.ime
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])

        with get_cursor() as cur:
            cur.execute(query, params)
            return [
                RestavracijaDto.from_dict(dict(vrstica))
                for vrstica in cur.fetchall()
            ]

    def stevilo_restavracij(
        self,
        iskanje: str | None = None,
        lokacija_id: int | None = None,
        kuhinja_id: int | None = None,
        dan_v_tednu: int | None = None,
        ima_telefon: bool = False,
        ima_spletno_stran: bool = False,
        ima_delovni_cas: bool = False,
    ) -> int:
        query = """
            SELECT COUNT(DISTINCT r.restavracija_id) AS stevilo
            FROM restavracija r
            JOIN lokacija l ON l.lokacija_id = r.lokacija_id
            LEFT JOIN restavracija_kuhinja rk
                ON rk.restavracija_id = r.restavracija_id
            LEFT JOIN kuhinja k ON k.kuhinja_id = rk.kuhinja_id
        """

        where = []
        params = []

        if iskanje:
            where.append(
                """
                (
                    LOWER(r.ime) LIKE LOWER(%s)
                    OR LOWER(l.ime_lokacije) LIKE LOWER(%s)
                    OR LOWER(k.vrsta) LIKE LOWER(%s)
                )
                """
            )
            vzorec = f"%{iskanje}%"
            params.extend([vzorec, vzorec, vzorec])

        if lokacija_id:
            where.append("r.lokacija_id = %s")
            params.append(lokacija_id)

        if kuhinja_id:
            where.append(
                """
                EXISTS (
                    SELECT 1
                    FROM restavracija_kuhinja rk2
                    WHERE rk2.restavracija_id = r.restavracija_id
                      AND rk2.kuhinja_id = %s
                )
                """
            )
            params.append(kuhinja_id)

        if dan_v_tednu:
            where.append(
                """
                EXISTS (
                    SELECT 1
                    FROM delovni_cas dc
                    WHERE dc.restavracija_id = r.restavracija_id
                      AND dc.dan_v_tednu = %s
                )
                """
            )
            params.append(dan_v_tednu)

        if ima_telefon:
            where.append("r.telefon IS NOT NULL AND TRIM(r.telefon) <> ''")

        if ima_spletno_stran:
            where.append(
                "r.spletna_stran IS NOT NULL AND TRIM(r.spletna_stran) <> ''"
            )

        if ima_delovni_cas:
            where.append(
                """
                EXISTS (
                    SELECT 1
                    FROM delovni_cas dc2
                    WHERE dc2.restavracija_id = r.restavracija_id
                )
                """
            )

        if where:
            query += " WHERE " + " AND ".join(where)

        with get_cursor() as cur:
            cur.execute(query, params)
            vrstica = cur.fetchone()
            return int(vrstica["stevilo"])

    def restavracija_po_id(
        self, restavracija_id: int
    ) -> RestavracijaDto | None:
        query = """
            SELECT
                r.restavracija_id,
                r.osm_id,
                r.osm_tip,
                r.ime,
                r.ulica,
                r.hisna_stevilka,
                r.telefon,
                r.spletna_stran,
                r.zemljepisna_sirina,
                r.zemljepisna_dolzina,
                r.opening_hours_raw,
                l.ime_lokacije,
                COALESCE(
                    STRING_AGG(DISTINCT k.vrsta, ', ' ORDER BY k.vrsta),
                    ''
                ) AS kuhinje
            FROM restavracija r
            JOIN lokacija l ON l.lokacija_id = r.lokacija_id
            LEFT JOIN restavracija_kuhinja rk
                ON rk.restavracija_id = r.restavracija_id
            LEFT JOIN kuhinja k ON k.kuhinja_id = rk.kuhinja_id
            WHERE r.restavracija_id = %s
            GROUP BY r.restavracija_id, l.ime_lokacije
        """

        with get_cursor() as cur:
            cur.execute(query, [restavracija_id])
            vrstica = cur.fetchone()
            return (
                RestavracijaDto.from_dict(dict(vrstica))
                if vrstica
                else None
            )

    def delovni_cas_restavracije(
        self, restavracija_id: int
    ) -> list[DelovniCas]:
        query = """
            SELECT
                delovni_cas_id,
                restavracija_id,
                dan_v_tednu,
                ura_od::text AS ura_od,
                ura_do::text AS ura_do
            FROM delovni_cas
            WHERE restavracija_id = %s
            ORDER BY dan_v_tednu, ura_od
        """

        with get_cursor() as cur:
            cur.execute(query, [restavracija_id])
            return [
                DelovniCas.from_dict(dict(vrstica))
                for vrstica in cur.fetchall()
            ]

    def vse_lokacije(self) -> list[Lokacija]:
        with get_cursor() as cur:
            cur.execute(
                """
                SELECT lokacija_id, ime_lokacije
                FROM lokacija
                ORDER BY ime_lokacije
                """
            )
            return [
                Lokacija.from_dict(dict(vrstica))
                for vrstica in cur.fetchall()
            ]

    def vse_kuhinje(self) -> list[Kuhinja]:
        with get_cursor() as cur:
            cur.execute(
                """
                SELECT kuhinja_id, vrsta
                FROM kuhinja
                ORDER BY vrsta
                """
            )
            return [
                Kuhinja.from_dict(dict(vrstica))
                for vrstica in cur.fetchall()
            ]
