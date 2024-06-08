from app.models.ibge import Distrito
from typing import Any, Callable, TypeVar
from pydantic import BaseModel
import requests

T = TypeVar("T", bound=BaseModel)


class IBGEService:
    def __init__(self) -> None:
        self.base_url = "https://servicodados.ibge.gov.br/api/v1"
        self.localidades_url = f"{self.base_url}/localidades"

    def _request_with_filter_and_pagination(
        self,
        url: str,
        page: int,
        per_page: int,
        filter: Callable[[dict[str, Any]], bool],
        model_constructor: Callable[[dict[str, Any]], T],
    ) -> list[T]:
        r = requests.get(url)
        r.raise_for_status()

        skip = (page - 1) * per_page
        skipped = 0
        data = []

        for d in r.json():
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

        return self._request_with_filter_and_pagination(
            f"{self.localidades_url}/distritos",
            page,
            per_page,
            lambda d: not search or d["nome"].lower().startswith(search),
            Distrito,
        )
