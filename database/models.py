from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.connection import Base


class Cidades(Base):
    __tablename__ = "cidades"

    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(45), nullable=False)
    agencias_bank = relationship("Agencias", backref="cidades")


class Agencias(Base):
    __tablename__ = "agencias"

    id: int = Column(Integer, primary_key=True, index=True)
    descricao: str = Column(String(50), nullable=True)
    sede: str = Column(String(45), nullable=False)
    cidades_id: int = Column(Integer, ForeignKey("cidades.id"), nullable=False)
    contas_bank = relationship("Contas", backref="agencias")


class Contas(Base):
    __tablename__ = "contas"

    id: int = Column(Integer, primary_key=True, index=True)
    agencias_id: int = Column(Integer, ForeignKey("agencias.id"), nullable=False)
    tipo_conta: str = Column(String(45), nullable=False)


class Clientes(Base):
    __tablename__ = "clientes"

    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(100), nullable=False)
    endereco: str = Column(String(100), nullable=False)
    cep: str = Column(String(9), nullable=False)
    telefone: str = Column(String(9), nullable=False)
    descricao: str = Column(String(50), nullable=True)


class Clientes_has_Contas(Base):
    __tablename__ = "clientes_has_contas"

    clientes_id: int = Column(Integer, ForeignKey("clientes.id"), primary_key=True, index=True)
    contas_id: int = Column(Integer, ForeignKey("contas.id"), primary_key=True, index=True)
