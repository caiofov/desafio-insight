from app.factories.ibge import get_ibge_service
from app.models.ibge import UF, Distrito, MunicipioType
from app.services.ibge import IBGEService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/distritos")
def list_distritos(
    page: int = 1,
    per_page: int = 20,
    search: str | None = None,
    service: IBGEService = Depends(get_ibge_service),
) -> list[Distrito]:
    return service.list_distritos(page, per_page, search)


@router.get("/estados")
def list_municipios(
    page: int = 1,
    per_page: int = 20,
    search: str | None = None,
    service: IBGEService = Depends(get_ibge_service),
) -> list[MunicipioType]:
    return service.list_municipios(page, per_page, search)


@router.get("/municipios/{id}")
def get_municipio(
    id: str | int,
    service: IBGEService = Depends(get_ibge_service),
) -> MunicipioType:
    return service.get_municipio(id)


@router.get("/estados")
def list_estados(
    search: str | None = None, service: IBGEService = Depends(get_ibge_service)
) -> list[UF]:
    return service.list_estados(search)


@router.get("/estados/{id}")
def get_estado(
    id: str | int,
    service: IBGEService = Depends(get_ibge_service),
) -> UF:
    return service.get_estado(id)
