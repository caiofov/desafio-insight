from app.factories.ibge import get_ibge_service
from app.models.localidades import UF, Distrito, MunicipioType
from app.services.ibge import IBGEService
from fastapi import APIRouter, Depends, Query

router = APIRouter()


@router.get("/distritos")
def list_distritos(
    page: int = 1,
    per_page: int = 20,
    search: str | None = None,
    service: IBGEService = Depends(get_ibge_service),
) -> list[Distrito]:
    """Lista todos os distritos com paginação e permite uma busca pelo nome

    - `page` (int, optional): Página atual da paginação.
    - `per_page` (int, optional): Tamanho da página da paginação.
    - `search` (str | None, optional): Nome a ser pesquisado. Dá match com o início do nome do distrito.

    """
    return service.list_distritos(page, per_page, search)


@router.get("/municipios")
def list_municipios(
    page: int = 1,
    per_page: int = 20,
    search: str | None = None,
    service: IBGEService = Depends(get_ibge_service),
) -> list[MunicipioType]:
    """Lista todos os municípios com paginação e permite uma busca pelo nome

    - `page` (int, optional): Página atual da paginação.
    - `per_page` (int, optional): Tamanho da página da paginação.
    - `search` (str | None, optional): Nome a ser pesquisado. Dá match com o início do nome do município. (não é case sensitive)

    """
    return service.list_municipios(page, per_page, search)


@router.get("/municipios/{id}")
def get_municipio(
    id: str,
    service: IBGEService = Depends(get_ibge_service),
) -> MunicipioType:
    """
    Retorna o município com o ID inserido.

    - `id` (str): ID do IBGE ou nome exato (não é case sensitive)

    #### Sobre os IDs do IBGE, veja mais em https://servicodados.ibge.gov.br/api/docs/localidades#api-bq
    """
    return service.get_municipio(id)


@router.get("/estados")
def list_estados(
    search: str | None = None,
    ids: list[int] = Query(None),
    service: IBGEService = Depends(get_ibge_service),
) -> list[UF]:
    """Lista todos os estados e permite busca pelo nome ou seleção pelo ID do IBGE
    #### Sobre os IDs do IBGE, veja mais em https://servicodados.ibge.gov.br/api/docs/localidades#api-bq

    - `search` (str | None, optional): Nome a ser pesquisado. Dá match com o início do nome do estado. (não é case sensitive)
    - `ids` (list[int], optional): IDS a serem selecionados.

    """
    return service.list_estados(search, ids)


@router.get("/estados/{id}")
def get_estado(
    id: str | int,
    service: IBGEService = Depends(get_ibge_service),
) -> UF:
    """
    Retorna o estado com o ID inserido.

    - `id` (str | int): ID do IBGE ou nome exato (não é case sensitive)

    #### Sobre os IDs do IBGE, veja mais em https://servicodados.ibge.gov.br/api/docs/localidades#api-bq
    """
    return service.get_estado(id)
