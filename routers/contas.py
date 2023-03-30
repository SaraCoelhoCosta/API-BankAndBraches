from sqlalchemy.orm import Session
from database.models import Contas
from services.contasServices import ContasService
from schemas.schema_contas import ContasResponse
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
import xml.etree.ElementTree as ET
import xmltodict
from database.connection import get_db

router = APIRouter()


@router.get("", response_model=list[ContasResponse])
def list(db: Session = Depends(get_db)):
    contas = ContasService.list(db)
    return [ContasResponse.from_orm(conta) for conta in contas]


@router.get("/{id}", response_model=ContasResponse)
def find_id(id: int, db: Session = Depends(get_db)):
    conta = ContasService.get_id(db, id)
    if not conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada!"
        )
    return ContasResponse.from_orm(conta)


@router.post("", response_model=ContasResponse, status_code=status.HTTP_201_CREATED)
async def create(request: Request, db: Session = Depends(get_db)):
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json = await request.json()
        conta = ContasService.save(db, Contas(**json))
        return ContasResponse.from_orm(conta)
    elif content_type == "application/xml":
        xml = await request.body()
        json = xmltodict.parse(xml)
        conta = ContasService.save(db, Contas(**json['contas']))
        return ContasResponse.from_orm(conta)


@router.put("/{id}", response_model=ContasResponse)
async def update(id: int, request: Request, db: Session = Depends(get_db)):
    if not ContasService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada!"
        )
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json = await request.json()
        conta = ContasService.save(db, Contas(**json))
        return ContasResponse.from_orm(conta)
    elif content_type == "application/xml":
        xml = await request.body()
        json = xmltodict.parse(xml)
        conta = ContasService.save(db, Contas(**json['contas']))
        return ContasResponse.from_orm(conta)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    if not ContasService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada!"
        )
    ContasService.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
