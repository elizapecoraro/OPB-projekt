from Data.database import get_cursor


class RestavracijaRepository:
    """Metode za branje podatkov o restavracijah iz baze."""

    def seznam_restavracij(self, iskanje: str | None = None, limit: int = 50):
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
                l.ime_lokacije
            FROM restavracija r
            JOIN lokacija l ON l.lokacija_id = r.lokacija_id
        """
        params: list[object] = []

        if iskanje:
            query += " WHERE LOWER(r.ime) LIKE LOWER(%s) OR LOWER(l.ime_lokacije) LIKE LOWER(%s)"
            params.extend([f"%{iskanje}%", f"%{iskanje}%"])

        query += " ORDER BY r.ime LIMIT %s"
        params.append(limit)

        with get_cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()

    def restavracija_po_id(self, restavracija_id: int):
        query = """
            SELECT
                r.*,
                l.ime_lokacije,
                COALESCE(STRING_AGG(k.vrsta, ', ' ORDER BY k.vrsta), '') AS kuhinje
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
