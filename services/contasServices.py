from sqlalchemy.orm import Session
from database.models import Contas


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
