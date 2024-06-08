from app.factories.ibge import get_ibge_service
from app.models.nomes import Nome, NomeLocalidade, NomeLocalidadeWithDetails
from app.services.ibge import IBGEService
from fastapi import APIRouter, Depends, Query

router = APIRouter()


@router.get("")
def get_names(
    names: list[str] = Query(),
    service: IBGEService = Depends(get_ibge_service),
) -> list[Nome]:
    """Dados dos nomes listados no IBGE

    - `names` (list[str]): Nomes para os quais os dados devem ser coletados

    """
    return service.get_names(names)


@router.get("/by_uf")
def get_name_by_uf(
    name: str,
    uf_name: bool = False,
    service: IBGEService = Depends(get_ibge_service),
) -> list[NomeLocalidade] | list[NomeLocalidadeWithDetails]:
    """Dados de um único nome, agrupados pela UF. Caso `uf_name` seja verdadeiro, retorna detalhes de cada UF

    - `name` (str): Nome para o qual os dados devem ser coletados
    - `uf_name` (bool, optional): Caso verdadeiro, retorna os dados de cada UF listada . Padrão é false

    """
    return service.get_name_by_uf(name, uf_name)
