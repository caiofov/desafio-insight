from typing import Any, Literal, overload
from app.models.ibge import Distrito, Municipio
from app.utils.types import RawJSONType
import requests
import abc


class IBGEClientBase(abc.ABC):
    def __init__(self, api_version: Literal[1, 2], api_path: str) -> None:
        self._base_url = (
            f"https://servicodados.ibge.gov.br/api/v{api_version}/{api_path}"
        )
        super().__init__()

    def _make_request(self, url: str, **kwargs: Any) -> Any:
        r = requests.get(f"{self._base_url}/{url}", **kwargs)
        r.raise_for_status()
        return r.json()


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
