from Data.database import get_cursor


class RestavracijaRepository:
    def seznam_restavracij(
        self,
        iskanje: str | None = None,
        lokacija_id: int | None = None,
        kuhinja_id: int | None = None,
        dan_v_tednu: int | None = None,
        ima_telefon: bool = False,
        ima_spletno_stran: bool = False,
        limit: int = 200,       #mogoč 100
    ):
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
                COALESCE(STRING_AGG(DISTINCT k.vrsta, ', ' ORDER BY k.vrsta), '') AS kuhinje
            FROM restavracija r
            JOIN lokacija l ON l.lokacija_id = r.lokacija_id
            LEFT JOIN restavracija_kuhinja rk ON rk.restavracija_id = r.restavracija_id
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
            params.extend([f"%{iskanje}%", f"%{iskanje}%", f"%{iskanje}%"])

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
            where.append("r.spletna_stran IS NOT NULL AND TRIM(r.spletna_stran) <> ''")

        if where:
            query += " WHERE " + " AND ".join(where)

        query += """
            GROUP BY r.restavracija_id, l.ime_lokacije
            ORDER BY r.ime
            LIMIT %s
        """
        params.append(limit)

        with get_cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()

    def restavracija_po_id(self, restavracija_id: int):
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
                COALESCE(STRING_AGG(DISTINCT k.vrsta, ', ' ORDER BY k.vrsta), '') AS kuhinje
            FROM restavracija r
            JOIN lokacija l ON l.lokacija_id = r.lokacija_id
            LEFT JOIN restavracija_kuhinja rk ON rk.restavracija_id = r.restavracija_id
            LEFT JOIN kuhinja k ON k.kuhinja_id = rk.kuhinja_id
            WHERE r.restavracija_id = %s
            GROUP BY r.restavracija_id, l.ime_lokacije
        """

        with get_cursor() as cur:
            cur.execute(query, [restavracija_id])
            return cur.fetchone()

    def delovni_cas_restavracije(self, restavracija_id: int):
        query = """
            SELECT
                delovni_cas_id,
                restavracija_id,
                dan_v_tednu,
                ura_od,
                ura_do
            FROM delovni_cas
            WHERE restavracija_id = %s
            ORDER BY dan_v_tednu, ura_od
        """

        with get_cursor() as cur:
            cur.execute(query, [restavracija_id])
            return cur.fetchall()

    def vse_lokacije(self):
        query = """
            SELECT lokacija_id, ime_lokacije
            FROM lokacija
            ORDER BY ime_lokacije
        """

        with get_cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    def vse_kuhinje(self):
        query = """
            SELECT kuhinja_id, vrsta
            FROM kuhinja
            ORDER BY vrsta
        """

        with get_cursor() as cur:
            cur.execute(query)
            return cur.fetchall()