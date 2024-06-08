from typing import Iterator
from app.services.ibge import IBGEService


def get_ibge_service() -> Iterator[IBGEService]:
    yield IBGEService()
