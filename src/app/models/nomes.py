from __future__ import annotations
from typing import Any
from pydantic import BaseModel, field_validator


class Periodo(BaseModel):
    start: int | None = None
    end: int

    @classmethod
    def from_str(cls, value: str) -> Periodo:
        # formato: '[YYYY,YYYY['ou 'YYYY['
        period = value.split(",")
        if len(period) == 1:
            return cls(end=int(period[0][:-1]))

        start, end = period
        return cls(start=int(start[1:]), end=int(end[:-1]))


class Registro(BaseModel):
    periodo: Periodo
    frequencia: int

    @field_validator("periodo", mode="before")
    def _parse_periodo(cls, value: Any) -> Periodo:
        if isinstance(value, str):
            return Periodo.from_str(value)
        return value


class Ocorrencia(BaseModel):
    populacao: int
    frequencia: int
    proporcao: float


class Nome(BaseModel):
    nome: str
    sexo: str | None
    localidade: str
    res: list[Registro]


class NomeLocalidade(BaseModel):
    localidade: int
    res: list[Ocorrencia]
