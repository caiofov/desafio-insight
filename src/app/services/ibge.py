from app.models.ibge import Distrito, Municipio
from typing import Any, Callable, TypeVar
from app.utils.ibge_client import IBGELocalidadesClient
from app.utils.types import RawJSONType
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class IBGEService:
    def __init__(self, _ibge_client: IBGELocalidadesClient) -> None:
        self.base_url = "https://servicodados.ibge.gov.br/api/v1"
        self.localidades_url = f"{self.base_url}/localidades"
        self.ibge_client = _ibge_client

    def _filter_and_pagination(
        self,
        raw_data: list[RawJSONType],
        page: int,
        per_page: int,
        filter: Callable[[dict[str, Any]], bool],
        model_constructor: Callable[[dict[str, Any]], T],
    ) -> list[T]:
        skip = (page - 1) * per_page
        skipped = 0
        data = []

        for d in raw_data:
            if len(data) >= per_page:
                break

            if not (accept := filter(d)):
                continue
            if accept and skipped < skip:
                skipped += 1
                continue

            data.append(model_constructor(**d))

        return data

    def list_distritos(
        self, page: int, per_page: int, search: str | None = None
    ) -> list[Distrito]:
        search = search.lower() if search else None  # not case sensitive
        raw_data = self.ibge_client.list_distritos()
        return self._filter_and_pagination(
            raw_data,
            page,
            per_page,
            lambda d: not search or d["nome"].lower().startswith(search),
            Distrito,
        )

    def list_municipios(
        self, page: int, per_page: int, search: str | None = None
    ) -> list[Municipio]:
        search = search.lower() if search else None  # not case sensitive
        raw_data = self.ibge_client.list_municipios()

        return self._filter_and_pagination(
            raw_data,
            page,
            per_page,
            lambda d: not search or d["nome"].lower().startswith(search),
            Municipio,
        )
