from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from database.models import Cidades
from database.connection import engine, Base, get_db
from services import CidadesService
from schemas import CidadesRequest, CidadesResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/cidades", response_model=list[CidadesResponse])
def list(db: Session = Depends(get_db)):
    cidades = CidadesService.list(db)
    return [CidadesResponse.from_orm(cidade) for cidade in cidades]


@app.get("/cidades/{id}", response_model=CidadesResponse)
def find_id(id: int, db: Session = Depends(get_db)):
    cidade = CidadesService.get_id(db, id)
    print(cidade)
    if not cidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cidade não encontrada!"
        )
    return CidadesResponse.from_orm(cidade)


@app.post("/cidades", response_model=CidadesResponse, status_code=status.HTTP_201_CREATED)
def create(request: CidadesRequest, db: Session = Depends(get_db)):
    cidade = CidadesService.save(db, Cidades(**request.dict()))
    return CidadesResponse.from_orm(cidade)


@app.put("/cidades/{id}", response_model=CidadesResponse)
def update(id: int, request: CidadesRequest, db: Session = Depends(get_db)):
    if not CidadesService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cidade não encontrada!"
        )
    curso = CidadesService.save(db, Cidades(**request.dict()))
    return CidadesResponse.from_orm(curso)


@app.delete("/cidades/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    if not CidadesService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cidade não encontrada!"
        )
    CidadesService.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

