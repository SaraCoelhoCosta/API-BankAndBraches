from pydantic import BaseModel


class CidadesResponse(BaseModel):
    id: int
    nome: str

    class Config:
        orm_mode = True
