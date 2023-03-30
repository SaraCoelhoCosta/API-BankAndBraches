from sqlalchemy.orm import Session
from database.models import Clientes
from services.services import ClientesService
from schemas.schema_clientes import ClientesResponse
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
import xml.etree.ElementTree as ET
import xmltodict
from database.connection import get_db

router = APIRouter()


@router.get("", response_model=list[ClientesResponse])
def list(db: Session = Depends(get_db)):
    clientes = ClientesService.list(db)
    return [ClientesResponse.from_orm(cliente) for cliente in clientes]


@router.get("/{id}", response_model=ClientesResponse)
def find_id(id: int, db: Session = Depends(get_db)):
    cliente = ClientesService.get_id(db, id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado!"
        )
    return ClientesResponse.from_orm(cliente)


@router.post("", response_model=ClientesResponse, status_code=status.HTTP_201_CREATED)
async def create(request: Request, db: Session = Depends(get_db)):
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json = await request.json()
        cliente = ClientesService.save(db, Clientes(**json))
        return ClientesResponse.from_orm(cliente)
    elif content_type == "application/xml":
        xml = await request.body()
        json = xmltodict.parse(xml)
        cliente = ClientesService.save(db, Clientes(**json['clientes']))
        return ClientesResponse.from_orm(cliente)


@router.put("/{id}", response_model=ClientesResponse)
async def update(id: int, request: Request, db: Session = Depends(get_db)):
    if not ClientesService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado!"
        )
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json = await request.json()
        cliente = ClientesService.save(db, Clientes(**json))
        return ClientesResponse.from_orm(cliente)
    elif content_type == "application/xml":
        xml = await request.body()
        json = xmltodict.parse(xml)
        cliente = ClientesService.save(db, Clientes(**json['clientes']))
        return ClientesResponse.from_orm(cliente)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    if not ClientesService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado!"
        )
    ClientesService.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
