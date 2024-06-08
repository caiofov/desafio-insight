from typing import Literal
from app.ibge_client.base import IBGEClientBase
from app.models.nomes import Nome, NomeLocalidade


class IBGENomesClient(IBGEClientBase):
    def __init__(self) -> None:
        super().__init__(2, "censos/nomes")

    def get_names(
        self,
        names: list[str],
        localidade: int | None = None,
        sex: Literal["F", "M"] | None = None,
    ) -> list[Nome]:
        params = {"localidade": localidade, "sexo": sex}
        params = {k: v for k, v in params.items() if v is not None}

        r = self._make_request("|".join(names), params=params)
        return [Nome(**n) for n in r]

    def get_name_grouped_by_uf(self, name: str) -> list[NomeLocalidade]:
        r = self._make_request(name, params={"groupBy": "UFs"})
        return [NomeLocalidade(**n) for n in r]
