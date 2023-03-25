from sqlalchemy.orm import Session
from database.models import Cidades
from services.services import CidadesService
from schemas.schemas import CidadesRequest, CidadesResponse
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
import xml.etree.ElementTree as ET
import xmltodict
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
async def create(request: Request, db: Session = Depends(get_db)):
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        cidade = CidadesService.save(db, Cidades(**request.dict()))
        return CidadesResponse.from_orm(cidade)
    elif content_type == "application/xml":
        xml = await request.body()
        json = xmltodict.parse(xml)
        cidade = CidadesService.save(db, Cidades(**json['cidades']))
        return CidadesResponse.from_orm(cidade)


@router.put("/{id}", response_model=CidadesResponse)
async def update(id: int, request: Request, db: Session = Depends(get_db)):
    if not CidadesService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cidade não encontrada!"
        )
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        cidade = CidadesService.save(db, Cidades(**request.dict()))
        return CidadesResponse.from_orm(cidade)
    elif content_type == "application/xml":
        xml = await request.body()
        json = xmltodict.parse(xml)
        cidade = CidadesService.save(db, Cidades(**json['cidades']))
        return CidadesResponse.from_orm(cidade)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    if not CidadesService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cidade não encontrada!"
        )
    CidadesService.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
