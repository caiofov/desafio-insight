from typing import Iterator
from app.services.ibge import IBGEService
from app.utils.ibge_client import IBGELocalidadesClient
from fastapi import Depends


def get_ibge_client() -> Iterator[IBGELocalidadesClient]:
    yield IBGELocalidadesClient()


def get_ibge_service(
    _ibge_client: IBGELocalidadesClient = Depends(get_ibge_client),
) -> Iterator[IBGEService]:
    yield IBGEService(_ibge_client)
