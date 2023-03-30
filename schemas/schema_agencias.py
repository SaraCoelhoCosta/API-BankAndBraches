from pydantic import BaseModel


class AgenciasResponse(BaseModel):
    id: int
    descricao: str
    sede: str
    cidades_id: int

    class Config:
        orm_mode = True

