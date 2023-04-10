from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.connection import Base


class Cidades(Base):
    __tablename__ = "cidades"

    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(45), nullable=False)
    agencias_bank = relationship("Agencias", cascade="all, delete")


class Agencias(Base):
    __tablename__ = "agencias"

    id: int = Column(Integer, primary_key=True, index=True)
    descricao: str = Column(String(50), nullable=True)
    sede: str = Column(String(45), nullable=False)
    cidades_id: int = Column(Integer, ForeignKey("cidades.id", ondelete="CASCADE"), nullable=False)
    contas_bank = relationship("Contas", cascade="all, delete")


class Contas(Base):
    __tablename__ = "contas"

    id: int = Column(Integer, primary_key=True, index=True)
    agencias_id: int = Column(Integer, ForeignKey("agencias.id", ondelete="CASCADE"), nullable=False)
    tipo_conta: str = Column(String(45), nullable=False)
    clientes_has_contas_bank = relationship("Clientes_has_Contas", cascade="all, delete")


class Clientes(Base):
    __tablename__ = "clientes"

    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(100), nullable=False)
    endereco: str = Column(String(100), nullable=False)
    cep: str = Column(String(9), nullable=False)
    telefone: str = Column(String(15), nullable=False)
    descricao: str = Column(String(50), nullable=True)
    clientes_has_contas_bank2 = relationship("Clientes_has_Contas", cascade="all, delete")


class Clientes_has_Contas(Base):
    __tablename__ = "clientes_has_contas"

    clientes_id: int = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False, primary_key=True, index=True)
    contas_id: int = Column(Integer, ForeignKey("contas.id", ondelete="CASCADE"), nullable=False, primary_key=True, index=True)
