from sqlalchemy.orm import Session
from database.models import Clientes_has_Contas
from services.clientes_has_contasServices import Clientes_has_ContasService
from schemas.schema_clientes_has_contas import ClientesHasContasResponse
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
import xml.etree.ElementTree as ET
import xmltodict
from database.connection import get_db

router = APIRouter()


@router.get("", response_model=list[ClientesHasContasResponse])
def list(db: Session = Depends(get_db)):
    clientes_has_contas = Clientes_has_ContasService.list(db)
    return [ClientesHasContasResponse.from_orm(cliente_has_conta) for cliente_has_conta in clientes_has_contas]


@router.get("/{id}", response_model=ClientesHasContasResponse)
def find_id(id: int, db: Session = Depends(get_db)):
    cliente_has_conta = Clientes_has_ContasService.get_id(db, id)
    if not cliente_has_conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente e conta não encontrados!"
        )
    return ClientesHasContasResponse.from_orm(cliente_has_conta)


@router.post("", response_model=ClientesHasContasResponse, status_code=status.HTTP_201_CREATED)
async def create(request: Request, db: Session = Depends(get_db)):
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json = await request.json()
        cliente_has_conta = Clientes_has_ContasService.save(db, Clientes_has_Contas(**json))
        return ClientesHasContasResponse.from_orm(cliente_has_conta)
    elif content_type == "application/xml":
        xml = await request.body()
        json = xmltodict.parse(xml)
        cliente_has_conta = Clientes_has_ContasService.save(db, Clientes_has_Contas(**json['clientes_has_contas']))
        return ClientesHasContasResponse.from_orm(cliente_has_conta)


@router.put("/{id}", response_model=ClientesHasContasResponse)
async def update(id: int, request: Request, db: Session = Depends(get_db)):
    if not Clientes_has_ContasService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente e conta não encontrados!"
        )
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json = await request.json()
        cliente_has_conta = Clientes_has_ContasService.save(db, Clientes_has_Contas(**json))
        return ClientesHasContasResponse.from_orm(cliente_has_conta)
    elif content_type == "application/xml":
        xml = await request.body()
        json = xmltodict.parse(xml)
        cliente_has_conta = Clientes_has_ContasService.save(db, Clientes_has_Contas(**json['clientes_has_contas']))
        return ClientesHasContasResponse.from_orm(cliente_has_conta)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    if not Clientes_has_ContasService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente e conta não encontrados!"
        )
    Clientes_has_ContasService.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
