from app.factories.ibge import get_ibge_service
from app.models.ibge import UF, Distrito, Municipio
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


@router.get("/municipios")
def list_municipios(
    page: int = 1,
    per_page: int = 20,
    search: str | None = None,
    service: IBGEService = Depends(get_ibge_service),
) -> list[Municipio]:
    return service.list_municipios(page, per_page, search)


@router.get("/estados")
def list_estados(
    search: str | None = None, service: IBGEService = Depends(get_ibge_service)
) -> list[UF]:
    return service.list_estados(search)
