from pydantic import BaseModel


class CidadesBase(BaseModel):
    id: int
    nome: str


class CidadesRequest(CidadesBase):
    id: int
    nome: str


class CidadesResponse(CidadesBase):
    id: int
    nome: str

    class Config:
        orm_mode = True
