from sqlalchemy.orm import Session
from database.models import Agencias
from services.agenciasServices import AgenciasService
from schemas.schema_agencias import AgenciasResponse
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
import xml.etree.ElementTree as ET
import xmltodict
from database.connection import get_db

router = APIRouter()


@router.get("", response_model=list[AgenciasResponse])
def list(db: Session = Depends(get_db)):
    agencias = AgenciasService.list(db)
    return [AgenciasResponse.from_orm(agencia) for agencia in agencias]


@router.get("/{id}", response_model=AgenciasResponse)
def find_id(id: int, db: Session = Depends(get_db)):
    agencia = AgenciasService.get_id(db, id)
    if not agencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agência não encontrada!"
        )
    return AgenciasResponse.from_orm(agencia)


@router.post("", response_model=AgenciasResponse, status_code=status.HTTP_201_CREATED)
async def create(request: Request, db: Session = Depends(get_db)):
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json = await request.json()
        agencia = AgenciasService.save(db, Agencias(**json))
        return AgenciasResponse.from_orm(agencia)
    elif content_type == "application/xml":
        xml = await request.body()
        json = xmltodict.parse(xml)
        agencia = AgenciasService.save(db, Agencias(**json['agencias']))
        return AgenciasResponse.from_orm(agencia)


@router.put("/{id}", response_model=AgenciasResponse)
async def update(id: int, request: Request, db: Session = Depends(get_db)):
    if not AgenciasService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agência não encontrada!"
        )
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json = await request.json()
        agencia = AgenciasService.save(db, Agencias(**json))
        return AgenciasResponse.from_orm(agencia)
    elif content_type == "application/xml":
        xml = await request.body()
        json = xmltodict.parse(xml)
        agencia = AgenciasService.save(db, Agencias(**json['agencias']))
        return AgenciasResponse.from_orm(agencia)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    if not AgenciasService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agência não encontrada!"
        )
    AgenciasService.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
