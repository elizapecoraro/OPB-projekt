from Data.restavracija_repository import RestavracijaRepository


class RestavracijaService:
    def __init__(self):
        self.repo = RestavracijaRepository()

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
        if iskanje is not None:
            iskanje = iskanje.strip()
            if iskanje == "":
                iskanje = None

        return self.repo.seznam_restavracij(
            iskanje=iskanje,
            lokacija_id=lokacija_id,
            kuhinja_id=kuhinja_id,
            dan_v_tednu=dan_v_tednu,
            ima_telefon=ima_telefon,
            ima_spletno_stran=ima_spletno_stran,
            ima_delovni_cas=ima_delovni_cas,
            limit=limit,
            offset=offset,
        )
    
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
        if iskanje is not None:
            iskanje = iskanje.strip()
            if iskanje == "":
                iskanje = None

        return self.repo.stevilo_restavracij(
            iskanje=iskanje,
            lokacija_id=lokacija_id,
            kuhinja_id=kuhinja_id,
            dan_v_tednu=dan_v_tednu,
            ima_telefon=ima_telefon,
            ima_spletno_stran=ima_spletno_stran,
            ima_delovni_cas=ima_delovni_cas,
        )

    def vse_lokacije(self):
        return self.repo.vse_lokacije()

    def vse_kuhinje(self):
        return self.repo.vse_kuhinje()

    def podrobnosti_restavracije(self, restavracija_id: int):
        return self.repo.restavracija_po_id(restavracija_id)

    def delovni_cas_restavracije(self, restavracija_id: int):
        return self.repo.delovni_cas_restavracije(restavracija_id)