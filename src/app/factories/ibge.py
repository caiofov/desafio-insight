from typing import Iterator
from app.services.ibge import IBGEService
from app.ibge_client import IBGELocalidadesClient, IBGENomesClient
from fastapi import Depends


def get_ibge_localidades_client() -> Iterator[IBGELocalidadesClient]:
    yield IBGELocalidadesClient()


def get_ibge_nomes_client() -> Iterator[IBGENomesClient]:
    yield IBGENomesClient()


def get_ibge_service(
    _ibge_localidades: IBGELocalidadesClient = Depends(get_ibge_localidades_client),
    _ibge_nomes: IBGENomesClient = Depends(get_ibge_nomes_client),
) -> Iterator[IBGEService]:
    yield IBGEService(_ibge_localidades, _ibge_nomes)
