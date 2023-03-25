from sqlalchemy.orm import Session
from database.models import Cidades
from services.services import CidadesService
from schemas.schemas import CidadesRequest, CidadesResponse
from fastapi import APIRouter, Depends, HTTPException, status, Response
from database.connection import get_db

router = APIRouter()


@router.get("", response_model=list[CidadesResponse])
def list(db: Session = Depends(get_db)):
    cidades = CidadesService.list(db)
    return [CidadesResponse.from_orm(cidade) for cidade in cidades]


@router.get("/{id}", response_model=CidadesResponse)
def find_id(id: int, db: Session = Depends(get_db)):
    cidade = CidadesService.get_id(db, id)
    if not cidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cidade não encontrada!"
        )
    return CidadesResponse.from_orm(cidade)


@router.post("", response_model=CidadesResponse, status_code=status.HTTP_201_CREATED)
def create(request: CidadesRequest, db: Session = Depends(get_db)):
    cidade = CidadesService.save(db, Cidades(**request.dict()))
    return CidadesResponse.from_orm(cidade)


@router.put("/{id}", response_model=CidadesResponse)
def update(id: int, request: CidadesRequest, db: Session = Depends(get_db)):
    if not CidadesService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cidade não encontrada!"
        )
    curso = CidadesService.save(db, Cidades(**request.dict()))
    return CidadesResponse.from_orm(curso)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    if not CidadesService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cidade não encontrada!"
        )
    CidadesService.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
