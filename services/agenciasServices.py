from sqlalchemy.orm import Session
from database.models import Agencias


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
    