"""Poslovna logika za prikaz in iskanje restavracij."""

from Data.restavracija_repository import RestavracijaRepository


class RestavracijaService:
    def __init__(self):
        self.repo = RestavracijaRepository()

    @staticmethod
    def _kot_slovar(objekt):
        return objekt.to_dict() if objekt is not None else None

    @classmethod
    def _kot_slovarji(cls, objekti):
        return [cls._kot_slovar(objekt) for objekt in objekti]

    @staticmethod
    def _uredi_iskanje(iskanje: str | None) -> str | None:
        if iskanje is None:
            return None
        iskanje = iskanje.strip()
        return iskanje or None

    def poisci_restavracije(
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
    ):
        rezultati = self.repo.seznam_restavracij(
            iskanje=self._uredi_iskanje(iskanje),
            lokacija_id=lokacija_id,
            kuhinja_id=kuhinja_id,
            dan_v_tednu=dan_v_tednu,
            ima_telefon=ima_telefon,
            ima_spletno_stran=ima_spletno_stran,
            ima_delovni_cas=ima_delovni_cas,
            limit=limit,
            offset=offset,
        )
        return self._kot_slovarji(rezultati)

    def stevilo_restavracij(
        self,
        iskanje: str | None = None,
        lokacija_id: int | None = None,
        kuhinja_id: int | None = None,
        dan_v_tednu: int | None = None,
        ima_telefon: bool = False,
        ima_spletno_stran: bool = False,
        ima_delovni_cas: bool = False,
    ):
        return self.repo.stevilo_restavracij(
            iskanje=self._uredi_iskanje(iskanje),
            lokacija_id=lokacija_id,
            kuhinja_id=kuhinja_id,
            dan_v_tednu=dan_v_tednu,
            ima_telefon=ima_telefon,
            ima_spletno_stran=ima_spletno_stran,
            ima_delovni_cas=ima_delovni_cas,
        )

    def vse_lokacije(self):
        return self._kot_slovarji(self.repo.vse_lokacije())

    def vse_kuhinje(self):
        return self._kot_slovarji(self.repo.vse_kuhinje())

    def podrobnosti_restavracije(self, restavracija_id: int):
        return self._kot_slovar(
            self.repo.restavracija_po_id(restavracija_id)
        )

    def delovni_cas_restavracije(self, restavracija_id: int):
        return self._kot_slovarji(
            self.repo.delovni_cas_restavracije(restavracija_id)
        )
