from Data.restavracija_repository import RestavracijaRepository


class RestavracijaService:
    """Aplikacijska logika za restavracije."""

    def __init__(self):
        self.repo = RestavracijaRepository()

    def poisci_restavracije(
        self,
        iskanje: str | None = None,
        lokacija_id: int | None = None,
        kuhinja_id: int | None = None,
    ):
        return self.repo.seznam_restavracij(
            iskanje=iskanje,
            lokacija_id=lokacija_id,
            kuhinja_id=kuhinja_id,
            limit=100,
        )
    
    def vse_lokacije(self):
        return self.repo.vse_lokacije()


    def vse_kuhinje(self):
        return self.repo.vse_kuhinje()

    def podrobnosti_restavracije(self, restavracija_id: int):
        return self.repo.restavracija_po_id(restavracija_id)
