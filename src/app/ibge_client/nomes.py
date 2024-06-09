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
        """Retorna dados dos nomes.

        Args:
            names (list[str]): Nomes para os quais os dados devem ser coletados
            localidade (int | None, optional): Filtrar por localidade (ID do IBGE). Defaults to None.
            sex (Literal['F', 'M'] | None, optional): Filtrar por sexo. Defaults to None.

        Returns:
            list[Nome]: Dados dos nomes
        """
        params = {"localidade": localidade, "sexo": sex}
        params = {k: v for k, v in params.items() if v is not None}

        r = self._make_request("|".join(names), params=params)
        return [Nome(**n) for n in r]

    def get_name_grouped_by_uf(self, name: str) -> list[NomeLocalidade]:
        """Retorna dados para um nome. Esses dados estão agrupados pela UF.

        Args:
            name (str): Nome para os quais os dados devem ser coletados

        Returns:
            list[NomeLocalidade]: Dados do nome
        """
        r = self._make_request(name, params={"groupBy": "UFs"})
        return [NomeLocalidade(**n) for n in r]
