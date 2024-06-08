from typing import Literal, overload
from app.ibge_client.base import IBGEClientBase
from app.models.localidades import (
    UF,
    Distrito,
    Municipio,
    MunicipioType,
    MunicipioWithImediata,
)
from app.utils.types import RawJSONType


class IBGELocalidadesClient(IBGEClientBase):
    def __init__(self) -> None:
        super().__init__(1, "localidades")

    @overload
    def list_distritos(
        self, return_model: bool = Literal[False]
    ) -> list[RawJSONType]: ...

    @overload
    def list_distritos(self, return_model: bool = Literal[True]) -> list[Distrito]: ...

    def list_distritos(
        self, return_model: bool = False
    ) -> list[RawJSONType] | list[Distrito]:
        distritos: list[RawJSONType] = self._make_request("distritos")

        return distritos if not return_model else [Distrito(**d) for d in distritos]

    def get_municipio(self, id: int) -> MunicipioType:
        r = self._make_request(f"municpios/{id}")
        return MunicipioWithImediata(**r) if "regiao-imediata" in r else Municipio(**r)

    @overload
    def list_municipios(
        self, return_model: bool = Literal[False]
    ) -> list[RawJSONType]: ...

    @overload
    def list_municipios(
        self, return_model: bool = Literal[True]
    ) -> list[Municipio]: ...

    def list_municipios(
        self, return_model: bool = False
    ) -> list[RawJSONType] | list[Municipio]:
        municipios: list[RawJSONType] = self._make_request("municipios")

        return municipios if not return_model else [Municipio(**d) for d in municipios]

    def get_estado(self, id: int) -> UF:
        r = self._make_request(f"estados/{id}")
        return UF(**r)

    @overload
    def list_estados(
        self, return_model: bool = Literal[False]
    ) -> list[RawJSONType]: ...

    @overload
    def list_estados(self, return_model: bool = Literal[True]) -> list[UF]: ...

    def list_estados(self, return_model: bool = False) -> list[RawJSONType] | list[UF]:
        estados: list[RawJSONType] = self._make_request("estados")

        return estados if not return_model else [UF(**d) for d in estados]
