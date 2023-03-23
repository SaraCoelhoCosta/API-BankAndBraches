from sqlalchemy import Column, Integer, String

from connection import Base


class Cidades(Base):
    __tablename__ = "cidades"

    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(45), nullable=False)
