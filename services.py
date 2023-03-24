from sqlalchemy.orm import Session
from database.models import Cidades


class CidadesService:
    @staticmethod
    def save(db: Session, cidade: Cidades) -> Cidades:
        print('Entrei')
        if cidade.id:
            db.merge(cidade)
        else:
            print('Salvou')
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
