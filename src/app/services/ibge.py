from app.models.ibge import Distrito
from typing import Any, Callable, TypeVar
from pydantic import BaseModel
import requests

T = TypeVar("T", bound=BaseModel)


class IBGEService:
    def __init__(self) -> None:
        self.base_url = "https://servicodados.ibge.gov.br/api/v1"
        self.localidades_url = f"{self.base_url}/localidades"

    def make_get_request_with_filter(
        self, url: str, filter: Callable[[dict[str, Any]], bool]
    ) -> list[dict[str, Any]]:
        r = requests.get(url)
        r.raise_for_status()

        return [r for r in r.json() if filter(r)]

    def pagination_with_models(
        self,
        data: list[dict[str, Any]],
        skip: int,
        per_page: int,
        model_constructor: Callable[[dict[str, Any]], T],
    ) -> list[T]:
        models = []
        for d in data[skip:]:
            if len(models) > per_page:
                break
            models.append(model_constructor(**d))
        return models

    def list_distritos(
        self, page: int, per_page: int, search: str | None = None
    ) -> list[Distrito]:
        skip = (page - 1) * per_page
        search = search.lower() if search else None  # not case sensitive

        raw = self.make_get_request_with_filter(
            f"{self.localidades_url}/distritos",
            lambda d: not search or d["nome"].lower().startswith(search),
        )

        # transform to base model and pagination
        return self.pagination_with_models(raw, skip, per_page, Distrito)
