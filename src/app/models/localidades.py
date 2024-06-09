from app.utils.enums import SiglaRegiao
from pydantic import BaseModel, Field


class Regiao(BaseModel):
    id: int
    nome: str
    sigla: SiglaRegiao


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
    regiao_intermediaria: RegiaoIntermediaria | None = Field(
        alias="regiao-intermediaria"
    )


class Mesorregiao(BaseModel):
    id: int
    nome: str


class Microrregiao(BaseModel):
    id: int
    nome: str
    mesorregiao: Mesorregiao | None = None


class MicrorregiaoWithImediata(Microrregiao):
    regiao_imediata: RegiaoImediata | None = Field(alias="regiao-imediata")


class Municipio(BaseModel):
    id: int
    nome: str
    microrregiao: Microrregiao | MicrorregiaoWithImediata | None = None


class MunicipioWithImediata(Municipio):
    microrregiao: Microrregiao | None = None
    regiao_imediata: RegiaoImediata = Field(alias="regiao-imediata")


MunicipioType = Municipio | MunicipioWithImediata


class Distrito(BaseModel):
    id: int
    nome: str
    municipio: Municipio
