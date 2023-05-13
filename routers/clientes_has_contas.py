from sqlalchemy.orm import Session
from database.models import Clientes_has_Contas
from services.clientes_has_contasServices import Clientes_has_ContasService
from schemas.schema_clientes_has_contas import ClientesHasContasResponse
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
import xml.etree.ElementTree as ET
import xmltodict
from database.connection import get_db

router = APIRouter()


@router.get("")
def list(request: Request, db: Session = Depends(get_db)):
    
    clientes_has_contas = Clientes_has_ContasService.list(db)

    # Verifica o formato da resposta
    accept = request.headers.get("Accept")
    if accept == "application/json" or accept == "text/plain" or accept == "*/*" or accept == "application/json, text/plain, */*":
        return [ClientesHasContasResponse.from_orm(cliente_has_conta) for cliente_has_conta in clientes_has_contas]
    
    elif accept == "application/xml" or accept == "text/plain" or accept == "*/*" or accept == "application/xml, text/plain, */*":    
        response_obj = [ClientesHasContasResponse.from_orm(cliente_has_conta) for cliente_has_conta in clientes_has_contas]

        root = ET.Element("clientes_has_contas")
        for cliente_has_conta in response_obj:
            cliente_has_conta_elem = ET.SubElement(root, "cliente_has_conta")
            ET.SubElement(cliente_has_conta_elem, "clientes_id").text = str(cliente_has_conta.clientes_id)
            ET.SubElement(cliente_has_conta_elem, "contas_id").text = str(cliente_has_conta.contas_id)
            
        xml_str = ET.tostring(root)

        return Response(content=xml_str, media_type="application/xml")


"""
@router.get("/{id}", response_model=ClientesHasContasResponse)
def find_id(request: Request, id: int, db: Session = Depends(get_db)):
    cliente_has_conta = Clientes_has_ContasService.get_id(db, id)
    if not cliente_has_conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente e conta não encontrados!"
        )

    root = ET.Element("cliente_has_conta")
    ET.SubElement(root, "clientes_id").text = str(cliente_has_conta.clientes_id)
    ET.SubElement(root, "contas_id").text = str(cliente_has_conta.contas_id)
    
    xml_str = ET.tostring(root)

    # Verifica o formato da resposta
    accept = request.headers.get("Accept")
    if accept == "application/json":
        return ClientesHasContasResponse.from_orm(cliente_has_conta)
    elif accept == "application/xml":    
        return Response(content=xml_str, media_type="application/xml")

"""


@router.post("")
async def create(request: Request, db: Session = Depends(get_db)):
    content_type = request.headers.get("Content-Type")
    accept = request.headers.get("Accept")
    
    # Verifica o formato da requisição
    if content_type == "application/json":
        json = await request.json()
        cliente_has_conta = Clientes_has_ContasService.save(db, Clientes_has_Contas(**json))
        
        # Verifica o formato da resposta
        if accept == "application/json" or accept == "text/plain" or accept == "*/*" or accept == "application/json, text/plain, */*":
            return ClientesHasContasResponse.from_orm(cliente_has_conta).json()
        
        elif accept == "application/xml" or accept == "text/plain" or accept == "*/*" or accept == "application/xml, text/plain, */*":
            xml = await request.body()
            json = xmltodict.parse(xml)
            cliente_has_conta = Clientes_has_ContasService.save(db, Clientes_has_Contas(**json['clientes_has_contas']))

            root = ET.Element("cliente_has_conta")
            ET.SubElement(root, "clientes_id").text = str(cliente_has_conta.clientes_id)
            ET.SubElement(root, "contas_id").text = str(cliente_has_conta.contas_id)
            
            xml_str = ET.tostring(root)    

            return Response(content=xml_str, media_type="application/xml")
    
    # Verifica o formato da requisição
    elif content_type == "application/xml":

        # Verifica o formato da resposta
        if accept == "application/json" or accept == "text/plain" or accept == "*/*" or accept == "application/json, text/plain, */*":
            return ClientesHasContasResponse.from_orm(cliente_has_conta)
        
        elif accept == "application/xml" or accept == "text/plain" or accept == "*/*" or accept == "application/xml, text/plain, */*":  
            xml = await request.body()
            json = xmltodict.parse(xml)
            cliente_has_conta = Clientes_has_ContasService.save(db, Clientes_has_Contas(**json['clientes_has_contas']))
            
            root = ET.Element("cliente_has_conta")
            ET.SubElement(root, "clientes_id").text = str(cliente_has_conta.clientes_id)
            ET.SubElement(root, "contas_id").text = str(cliente_has_conta.contas_id)
            
            xml_str = ET.tostring(root) 

            return Response(content=xml_str, media_type="application/xml")

"""
@router.put("/{id}", response_model=ClientesHasContasResponse)
async def update(id: int, request: Request, db: Session = Depends(get_db)):
    if not Clientes_has_ContasService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente e conta não encontrados!"
        )
    content_type = request.headers.get("Content-Type")
    accept = request.headers.get("Accept")
    
    # Verifica o formato da requisição
    if content_type == "application/json":
        json = await request.json()
        cliente_has_conta = Clientes_has_ContasService.save(db, Clientes_has_Contas(**json))
        
        root = ET.Element("cliente_has_conta")
        ET.SubElement(root, "clientes_id").text = str(cliente_has_conta.clientes_id)
        ET.SubElement(root, "contas_id").text = str(cliente_has_conta.contas_id)
        
        xml_str = ET.tostring(root)

        # Verifica o formato da resposta
        if accept == "application/json":
            return ClientesHasContasResponse.from_orm(cliente_has_conta)
        elif accept == "application/xml":    
            return Response(content=xml_str, media_type="application/xml")
    elif content_type == "application/xml":
        xml = await request.body()
        json = xmltodict.parse(xml)
        cliente_has_conta = Clientes_has_ContasService.save(db, Clientes_has_Contas(**json['clientes_has_contas']))
        # Verifica o formato da resposta
        if accept == "application/json":
            return ClientesHasContasResponse.from_orm(cliente_has_conta)
        elif accept == "application/xml":    
            return Response(content=cliente_has_conta.to_xml(), media_type="application/xml")
"""        
"""
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    if not Clientes_has_ContasService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente e conta não encontrados!"
        )
    Clientes_has_ContasService.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
"""