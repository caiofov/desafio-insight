from app.ibge_client.base import IBGEClientBase
from app.models.nomes import Nome


class IBGENomesClient(IBGEClientBase):
    def __init__(self) -> None:
        super().__init__(2, "censos/nomes")

    def get_names(self, names: list[str]) -> list[Nome]:
        return [Nome(**n) for n in self._make_request("|".join(names))]
