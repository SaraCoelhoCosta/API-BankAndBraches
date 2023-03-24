from sqlalchemy.orm import Session
from database.models import Cidades


class CidadesService:
    @staticmethod
    def create(db: Session, cidade: Cidades) -> Cidades:
        db.add(cidade)
        db.commit()
        return cidade

    @staticmethod
    def update(db: Session,  cidade: Cidades) -> Cidades:
        db.merge(cidade)
        db.commit()
        return cidade

    @staticmethod
    def delete(db: Session, id: int) -> None:
        cidade = db.query(Cidades).where(Cidades.id == id)
        if cidade is not None:
            db.delete(cidade)
            db.commit()
    
    @staticmethod
    def get_all(db: Session) -> list[Cidades]:
        return db.query(Cidades).all()
    
    @staticmethod
    def get_id(db: Session, id: int) -> Cidades:
        return db.query(Cidades).filter(Cidades.id == id)

    @staticmethod
    def exists_id(db: Session, id: int) -> bool:
        return db.query(Cidades).exists(id) is not None
