from pydantic import BaseModel


class ContasResponse(BaseModel):
    id: int
    agencias_id: int
    tipo_conta: str 

    class Config:
        orm_mode = True

