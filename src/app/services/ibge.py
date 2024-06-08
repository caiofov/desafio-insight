from app.models.localidades import (
    UF,
    Distrito,
    Municipio,
    MunicipioType,
    MunicipioWithImediata,
)
from typing import Any, Callable, Literal, TypeVar, overload
from app.models import Nome, NomeLocalidade, NomeLocalidadeWithDetails
from app.utils.errors import ItemNotFound
from app.ibge_client import IBGELocalidadesClient, IBGENomesClient
from app.utils.types import RawJSONType
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class IBGEService:
    def __init__(
        self, _ibge_localidades: IBGELocalidadesClient, _ibge_nomes: IBGENomesClient
    ) -> None:
        self.ibge_client = _ibge_localidades
        self.ibge_nomes = _ibge_nomes

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

    def get_municipio(self, id: int | str) -> MunicipioType:
        if isinstance(id, int):
            return self.ibge_client.get_municipio(id)
        raw_data = self.ibge_client.list_municipios()

        id = id.lower()  # not case sensitive

        for data in raw_data:
            if data["nome"].lower() == id:
                return (
                    MunicipioWithImediata(**data)
                    if "regiao-imediata" in data
                    else Municipio(**data)
                )

        raise ItemNotFound(f"Municipio - id: {id}")

    def list_estados(
        self, search: str | None = None, ids: list[int] | None = None
    ) -> list[UF]:
        search = search.lower() if search else None  # not case sensitive
        raw_data = self.ibge_client.list_estados(ids)

        data = []
        for d in raw_data:
            if not search or d["nome"].lower().startswith(search):
                data.append(UF(**d))
        return data

    def get_estado(self, id: int | str) -> UF:
        if isinstance(id, int):
            return self.ibge_client.get_estado(id)
        raw_data = self.ibge_client.list_estados()

        id = id.lower()  # not case sensitive

        for data in raw_data:
            if data["nome"].lower() == id:
                return UF(**data)

        raise ItemNotFound(f"UF - id: {id}")

    def get_names(self, names: list[str]) -> list[Nome]:
        return self.ibge_nomes.get_names(names)

    @overload
    def get_name_by_uf(
        self, name: str, include_uf_name: Literal[False] = False
    ) -> list[NomeLocalidade]: ...

    @overload
    def get_name_by_uf(
        self, name: str, include_uf_name: Literal[True] = True
    ) -> list[NomeLocalidadeWithDetails]: ...

    def get_name_by_uf(
        self, name: str, include_uf_name: bool = False
    ) -> list[NomeLocalidade] | list[NomeLocalidadeWithDetails]:
        data = self.ibge_nomes.get_name_grouped_by_uf(name)
        if not include_uf_name:
            return data
        estados = {
            e.id: e
            for e in self.ibge_client.list_estados([d.localidade for d in data], True)
        }
        return [
            NomeLocalidadeWithDetails.create(d, estados[d.localidade]) for d in data
        ]
