from typing import Any, Literal
import requests
import abc


class IBGEClientBase(abc.ABC):
    def __init__(self, api_version: Literal[1, 2], api_path: str) -> None:
        self._base_url = (
            f"https://servicodados.ibge.gov.br/api/v{api_version}/{api_path}"
        )
        super().__init__()

    def _make_request(self, url: str, method: str = "GET", **kwargs: Any) -> Any:
        r = requests.request(method, f"{self._base_url}/{url}", **kwargs)
        r.raise_for_status()
        return r.json()
