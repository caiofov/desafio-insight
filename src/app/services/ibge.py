from app.models.ibge import Distrito
from typing import Any
import requests


class IBGEService:
    def __init__(self) -> None:
        self.base_url = "https://servicodados.ibge.gov.br/api/v1"
        self.localidades_url = f"{self.base_url}/localidades"

    def list_distritos(
        self, page: int, per_page: int, order_by: str | None = None
    ) -> list[Distrito]:
        r = requests.get(f"{self.localidades_url}/distritos")
        r.raise_for_status()
        skip = (page - 1) * per_page
        raw: list[dict[str, Any]] = r.json()

        distritos = []
        for d in raw[skip:]:
            if len(distritos) > per_page:
                break
            distritos.append(Distrito(**d))

        return distritos
