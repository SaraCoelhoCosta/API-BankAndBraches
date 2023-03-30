from pydantic import BaseModel


class ClientesResponse(BaseModel):
    id: int
    nome: str
    endereco: str 
    cep: str
    telefone: str
    descricao: str

    class Config:
        orm_mode = True

