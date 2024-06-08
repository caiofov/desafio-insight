from app.factories.ibge import get_ibge_service
from app.models.nomes import Nome, NomeLocalidade, NomeLocalidadeWithDetails
from app.services.ibge import IBGEService
from fastapi import APIRouter, Depends, Query

router = APIRouter()


@router.get("")
def get_names(
    names: list[str] = Query(None),
    service: IBGEService = Depends(get_ibge_service),
) -> list[Nome]:
    return service.get_names(names)


@router.get("/by_uf")
def get_name_by_uf(
    name: str,
    uf_name: bool = False,
    service: IBGEService = Depends(get_ibge_service),
) -> list[NomeLocalidade] | list[NomeLocalidadeWithDetails]:
    return service.get_name_by_uf(name, uf_name)
