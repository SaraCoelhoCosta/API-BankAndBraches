from sqlalchemy.orm import Session
from database.models import Cidades
from database.models import Agencias
from database.models import Contas
from database.models import Clientes
from database.models import Clientes_has_Contas


class CidadesService:
    @staticmethod
    def save(db: Session, cidade: Cidades) -> Cidades:
        if cidade.id:
            db.merge(cidade)
        else:
            db.add(cidade)
        db.commit()
        return cidade

    @staticmethod
    def delete(db: Session, id: int) -> None:
        cidade = db.query(Cidades).where(Cidades.id == id).first()
        if cidade is not None:
            db.delete(cidade)
            db.commit()
    
    @staticmethod
    def list(db: Session) -> list[Cidades]:
        return db.query(Cidades).all()
    
    @staticmethod
    def get_id(db: Session, id: int) -> Cidades:
        return db.query(Cidades).filter(Cidades.id == id).first()

    @staticmethod
    def exists_id(db: Session, id: int) -> bool:
        return db.query(Cidades).filter(Cidades.id == id).first() is not None

class AgenciasService:
    @staticmethod
    def save(db: Session, agencia: Agencias) -> Agencias:
        if agencia.id:
            db.merge(agencia)
        else:
            db.add(agencia)
        db.commit()
        return agencia

    @staticmethod
    def delete(db: Session, id: int) -> None:
        agencia = db.query(Agencias).where(Agencias.id == id).first()
        if agencia is not None:
            db.delete(agencia)
            db.commit()
    
    @staticmethod
    def list(db: Session) -> list[Agencias]:
        return db.query(Agencias).all()
    
    @staticmethod
    def get_id(db: Session, id: int) -> Agencias:
        return db.query(Agencias).filter(Agencias.id == id).first()

    @staticmethod
    def exists_id(db: Session, id: int) -> bool:
        return db.query(Agencias).filter(Agencias.id == id).first() is not None
    
class ContasService:
    @staticmethod
    def save(db: Session, conta: Contas) -> Contas:
        if conta.id:
            db.merge(conta)
        else:
            db.add(conta)
        db.commit()
        return conta

    @staticmethod
    def delete(db: Session, id: int) -> None:
        conta = db.query(Contas).where(Contas.id == id).first()
        if conta is not None:
            db.delete(conta)
            db.commit()
    
    @staticmethod
    def list(db: Session) -> list[Contas]:
        return db.query(Contas).all()
    
    @staticmethod
    def get_id(db: Session, id: int) -> Contas:
        return db.query(Contas).filter(Contas.id == id).first()

    @staticmethod
    def exists_id(db: Session, id: int) -> bool:
        return db.query(Contas).filter(Contas.id == id).first() is not None
    
class ClientesService:
    @staticmethod
    def save(db: Session, cliente: Clientes) -> Clientes:
        if cliente.id:
            db.merge(cliente)
        else:
            db.add(cliente)
        db.commit()
        return cliente

    @staticmethod
    def delete(db: Session, id: int) -> None:
        cliente = db.query(Clientes).where(Clientes.id == id).first()
        if cliente is not None:
            db.delete(cliente)
            db.commit()
    
    @staticmethod
    def list(db: Session) -> list[Clientes]:
        return db.query(Clientes).all()
    
    @staticmethod
    def get_id(db: Session, id: int) -> Clientes:
        return db.query(Clientes).filter(Clientes.id == id).first()

    @staticmethod
    def exists_id(db: Session, id: int) -> bool:
        return db.query(Clientes).filter(Clientes.id == id).first() is not None
    
class Clientes_has_ContasService:
    @staticmethod
    def save(db: Session, cliente_tem_conta: Clientes_has_Contas) -> Clientes_has_Contas:
        if cliente_tem_conta.id:
            db.merge(cliente_tem_conta)
        else:
            db.add(cliente_tem_conta)
        db.commit()
        return cliente_tem_conta

    @staticmethod
    def delete(db: Session, id: int) -> None:
        cliente_tem_conta = db.query(Clientes_has_Contas).where(Clientes_has_Contas.id == id).first()
        if cliente_tem_conta is not None:
            db.delete(cliente_tem_conta)
            db.commit()
    
    @staticmethod
    def list(db: Session) -> list[Clientes_has_Contas]:
        return db.query(Clientes_has_Contas).all()
    
    @staticmethod
    def get_id(db: Session, id: int) -> Clientes_has_Contas:
        return db.query(Clientes_has_Contas).filter(Clientes_has_Contas.id == id).first()

    @staticmethod
    def exists_id(db: Session, id: int) -> bool:
        return db.query(Clientes_has_Contas).filter(Clientes_has_Contas.id == id).first() is not None