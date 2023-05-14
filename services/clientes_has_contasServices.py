from sqlalchemy import null
from sqlalchemy.orm import Session
from database.models import Clientes_has_Contas


class Clientes_has_ContasService:
    @staticmethod
    def save(db: Session, cliente_tem_conta: Clientes_has_Contas, id: int) -> Clientes_has_Contas:
        if id is not null:
            result = db.query(Clientes_has_Contas).where(Clientes_has_Contas.clientes_id == id).first()
            result.contas_id = cliente_tem_conta.contas_id
            # db.merge(cliente_tem_conta)
        else:
            db.add(cliente_tem_conta)
        db.commit()
        return cliente_tem_conta

    @staticmethod
    def delete(db: Session, id: int) -> None:
        cliente_tem_conta = db.query(Clientes_has_Contas).where(Clientes_has_Contas.clientes_id == id).first()
        if cliente_tem_conta is not None:
            db.delete(cliente_tem_conta)
            db.commit()
    
    @staticmethod
    def list(db: Session) -> list[Clientes_has_Contas]:
        return db.query(Clientes_has_Contas).all()
    
    @staticmethod
    def get_id(db: Session, id: int) -> Clientes_has_Contas:
        return db.query(Clientes_has_Contas).filter(Clientes_has_Contas.clientes_id == id).first()

    @staticmethod
    def exists_id(db: Session, id: int) -> bool:
        return db.query(Clientes_has_Contas).filter(Clientes_has_Contas.clientes_id == id).first() is not None