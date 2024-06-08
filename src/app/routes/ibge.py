from app.factories.ibge import get_ibge_service
from app.models.ibge import Distrito
from app.services.ibge import IBGEService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/distritos")
def list_distritos(
    page: int = 1,
    per_page: int = 20,
    order_by: str | None = None,
    service: IBGEService = Depends(get_ibge_service),
) -> list[Distrito]:
    return service.list_distritos(page, per_page, order_by)
