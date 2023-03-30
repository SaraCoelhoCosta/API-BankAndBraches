from pydantic import BaseModel


class ClientesHasContasResponse(BaseModel):
    clientes_id: int
    contas_id: int

    class Config:
        orm_mode = True

