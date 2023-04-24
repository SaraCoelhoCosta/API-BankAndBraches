from sqlalchemy.orm import Session
from database.models import Clientes
from services.clientesServices import ClientesService
from schemas.schema_clientes import ClientesResponse
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
import xml.etree.ElementTree as ET
import xmltodict
from database.connection import get_db

router = APIRouter()


@router.get("", response_model=list[ClientesResponse])
def list(request: Request, db: Session = Depends(get_db)):
    clientes = ClientesService.list(db)
    response_obj = [ClientesResponse.from_orm(cliente) for cliente in clientes]

    root = ET.Element("clientes")
    for cliente in response_obj:
        cliente_elem = ET.SubElement(root, "cliente")
        ET.SubElement(cliente_elem, "id").text = str(cliente.id)
        ET.SubElement(cliente_elem, "nome").text = cliente.nome
        ET.SubElement(cliente_elem, "endereco").text = cliente.endereco
        ET.SubElement(cliente_elem, "cep").text = cliente.cep
        ET.SubElement(cliente_elem, "telefone").text = cliente.telefone
        ET.SubElement(cliente_elem, "descricao").text = cliente.descricao
        
        xml_str = ET.tostring(root)

    # Verifica o formato da resposta
    accept = request.headers.get("Accept")
    if accept == "application/json":
        return [ClientesResponse.from_orm(cliente) for cliente in clientes]
    elif accept == "application/xml":    
        return Response(content=xml_str, media_type="application/xml")


@router.get("/{id}", response_model=ClientesResponse)
def find_id(request: Request, id: int, db: Session = Depends(get_db)):
    cliente = ClientesService.get_id(db, id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado!"
        )

    root = ET.Element("cliente")
    ET.SubElement(root, "id").text = str(cliente.id)
    ET.SubElement(root, "nome").text = cliente.nome
    ET.SubElement(root, "endereco").text = cliente.endereco
    ET.SubElement(root, "cep").text = cliente.cep
    ET.SubElement(root, "telefone").text = cliente.telefone
    ET.SubElement(root, "descricao").text = cliente.descricao
    
    xml_str = ET.tostring(root)

    # Verifica o formato da resposta
    accept = request.headers.get("Accept")
    if accept == "application/json":
        return ClientesResponse.from_orm(cliente)
    elif accept == "application/xml":    
        return Response(content=xml_str, media_type="application/xml")


@router.post("", response_model=ClientesResponse, status_code=status.HTTP_201_CREATED)
async def create(request: Request, db: Session = Depends(get_db)):
    content_type = request.headers.get("Content-Type")
    accept = request.headers.get("Accept")
    
    # Verifica o formato da requisição
    if content_type == "application/json":
        json = await request.json()
        cliente = ClientesService.save(db, Clientes(**json))
        # Verifica o formato da resposta
        if accept == "application/json":
            return ClientesResponse.from_orm(cliente)
        elif accept == "application/xml":    
            return Response(content=xml_str, media_type="application/xml")
    elif content_type == "application/xml":
        xml = await request.body()
        json = xmltodict.parse(xml)
        cliente = ClientesService.save(db, Clientes(**json['clientes']))

        root = ET.Element("cliente")
        ET.SubElement(root, "id").text = str(cliente.id)
        ET.SubElement(root, "nome").text = cliente.nome
        ET.SubElement(root, "endereco").text = cliente.endereco
        ET.SubElement(root, "cep").text = cliente.cep
        ET.SubElement(root, "telefone").text = cliente.telefone
        ET.SubElement(root, "descricao").text = cliente.descricao
        
        xml_str = ET.tostring(root)

        # Verifica o formato da resposta
        if accept == "application/json":
            return ClientesResponse.from_orm(cliente)
        elif accept == "application/xml":    
            return Response(content=xml_str, media_type="application/xml")


@router.put("/{id}", response_model=ClientesResponse)
async def update(id: int, request: Request, db: Session = Depends(get_db)):
    if not ClientesService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado!"
        )
    content_type = request.headers.get("Content-Type")
    accept = request.headers.get("Accept")
    
    # Verifica o formato da requisição
    if content_type == "application/json":
        json = await request.json()
        cliente = ClientesService.save(db, Clientes(**json))

        root = ET.Element("cliente")
        ET.SubElement(root, "id").text = str(cliente.id)
        ET.SubElement(root, "nome").text = cliente.nome
        ET.SubElement(root, "endereco").text = cliente.endereco
        ET.SubElement(root, "cep").text = cliente.cep
        ET.SubElement(root, "telefone").text = cliente.telefone
        ET.SubElement(root, "descricao").text = cliente.descricao
        
        xml_str = ET.tostring(root)

        # Verifica o formato da resposta
        if accept == "application/json":
            return ClientesResponse.from_orm(cliente)
        elif accept == "application/xml":    
            return Response(content=xml_str.decode("utf-8"), media_type="application/xml")
    elif content_type == "application/xml":
        xml = await request.body()
        json = xmltodict.parse(xml)
        cliente = ClientesService.save(db, Clientes(**json['clientes']))
        # Verifica o formato da resposta
        if accept == "application/json":
            return ClientesResponse.from_orm(cliente)
        elif accept == "application/xml":    
            return Response(content=cliente.to_xml(), media_type="application/xml")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    if not ClientesService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado!"
        )
    ClientesService.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
