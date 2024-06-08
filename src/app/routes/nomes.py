from app.factories.ibge import get_ibge_service
from app.models.nomes import Nome
from app.services.ibge import IBGEService
from fastapi import APIRouter, Depends, Query

router = APIRouter()


@router.get("")
def list_municipios(
    names: list[str] = Query(None),
    service: IBGEService = Depends(get_ibge_service),
) -> list[Nome]:
    return service.get_names(names)
