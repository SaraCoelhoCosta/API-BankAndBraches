from sqlalchemy.orm import Session
from database.models import Clientes

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
    def list(db: Session):
        cidades = db.query(Clientes).all()
        return cidades
    
    @staticmethod
    def get_id(db: Session, id: int) -> Clientes:
        return db.query(Clientes).filter(Clientes.id == id).first()

    @staticmethod
    def exists_id(db: Session, id: int) -> bool:
        return db.query(Clientes).filter(Clientes.id == id).first() is not None
    