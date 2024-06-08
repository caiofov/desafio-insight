from pydantic import BaseModel


class Regiao(BaseModel):
    id: int
    nome: str
    sigla: str


class UF(BaseModel):
    id: int
    nome: str
    sigla: str
    regiao: Regiao


class RegiaoIntermediaria(BaseModel):
    id: int
    nome: str
    UF: UF


class RegiaoImediata(BaseModel):
    id: int
    nome: str
    regiao_intermediaria: RegiaoIntermediaria | None


class Mesorregiao(BaseModel):
    id: int
    nome: str


class Microrregiao(BaseModel):
    id: int
    nome: str
    mesorregiao: Mesorregiao | None


class MicrorregiaoWithImediata(Microrregiao):
    regiao_imediata: RegiaoImediata | None


class Municipio(BaseModel):
    id: int
    nome: str
    microrregiao: Microrregiao | MicrorregiaoWithImediata | None


class MunicipioWithImediata(BaseModel):
    microrregiao: Microrregiao | None
    regiao_imediata: RegiaoImediata | None


class Distrito(BaseModel):
    id: int
    nome: str
    municipio: Municipio
