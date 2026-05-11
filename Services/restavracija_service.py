from Data.restavracija_repository import RestavracijaRepository


class RestavracijaService:
    """Aplikacijska logika za restavracije."""

    def __init__(self):
        self.repo = RestavracijaRepository()

    def poisci_restavracije(self, iskanje: str | None = None):
        return self.repo.seznam_restavracij(iskanje=iskanje, limit=100)

    def podrobnosti_restavracije(self, restavracija_id: int):
        return self.repo.restavracija_po_id(restavracija_id)
