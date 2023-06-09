from sqlalchemy.orm import Session
from database.models import Contas
from services.contasServices import ContasService
from schemas.schema_contas import ContasResponse
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
import xml.etree.ElementTree as ET
import xmltodict
from database.connection import get_db

router = APIRouter()


@router.get("")
def list(request: Request, db: Session = Depends(get_db)):
    
    contas = ContasService.list(db)

    # Verifica o formato da resposta
    accept = request.headers.get("Accept")
    if accept == "application/json" or accept == "text/plain" or accept == "*/*" or accept == "application/json, text/plain, */*":
        return [ContasResponse.from_orm(conta) for conta in contas]
    
    elif accept == "application/xml" or accept == "text/plain" or accept == "*/*" or accept == "application/xml, text/plain, */*":    
        response_obj = [ContasResponse.from_orm(conta) for conta in contas]

        root = ET.Element("contas")
        for conta in response_obj:
            conta_elem = ET.SubElement(root, "conta")
            ET.SubElement(conta_elem, "id").text = str(conta.id)
            ET.SubElement(conta_elem, "agencias_id").text = str(conta.agencias_id)
            ET.SubElement(conta_elem, "tipo_conta").text = conta.tipo_conta
        
        xml_str = ET.tostring(root)
        return Response(content=xml_str, media_type="application/xml")


@router.get("/{id}")
def find_id(request: Request, id: int, db: Session = Depends(get_db)):
    conta = ContasService.get_id(db, id)
    if not conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada!"
        )
    
    # Verifica o formato da resposta
    accept = request.headers.get("Accept")
    if accept == "application/json" or accept == "text/plain" or accept == "*/*" or accept == "application/json, text/plain, */*":
        return ContasResponse.from_orm(conta)
    
    elif accept == "application/xml" or accept == "text/plain" or accept == "*/*" or accept == "application/xml, text/plain, */*":    
        response_obj = ContasResponse.from_orm(conta)

        root = ET.Element("contas")
        conta_elem = ET.SubElement(root, "conta")
        ET.SubElement(conta_elem, "id").text = str(conta.id)
        ET.SubElement(conta_elem, "agencias_id").text = str(conta.agencias_id)
        ET.SubElement(conta_elem, "tipo_conta").text = conta.tipo_conta
        
        xml_str = ET.tostring(root)
        return Response(content=xml_str, media_type="application/xml")


@router.post("")
async def create(request: Request, db: Session = Depends(get_db)):
    content_type = request.headers.get("Content-Type")
    accept = request.headers.get("Accept")
    
    # Verifica o formato da requisição
    if content_type == "application/json":
        json = await request.json()
        conta = ContasService.save(db, Contas(**json))

        # Verifica o formato da resposta
        if accept == "application/json" or accept == "text/plain" or accept == "*/*" or accept == "application/json, text/plain, */*":
            return ContasResponse.from_orm(conta).json()
        
        elif accept == "application/xml" or accept == "text/plain" or accept == "*/*" or accept == "application/xml, text/plain, */*":  
            xml = await request.body()
            json = xmltodict.parse(xml)
            conta = ContasService.save(db, Contas(**json['contas']))
            
            root = ET.Element("conta")
            ET.SubElement(root, "id").text = str(conta.id)
            ET.SubElement(root, "agencias_id").text = str(conta.agencias_id)
            ET.SubElement(root, "tipo_conta").text = conta.tipo_conta

            return Response(content=xml_str, media_type="application/xml")
        
    # Verifica o formato da requisição
    elif content_type == "application/xml":

        # Verifica o formato da resposta
        if accept == "application/json" or accept == "text/plain" or accept == "*/*" or accept == "application/json, text/plain, */*":
            return ContasResponse.from_orm(conta)
        
        elif accept == "application/xml" or accept == "text/plain" or accept == "*/*" or accept == "application/xml, text/plain, */*": 
            xml = await request.body()
            json = xmltodict.parse(xml)
            conta = ContasService.save(db, Contas(**json['contas']))
            
            root = ET.Element("conta")
            ET.SubElement(root, "id").text = str(conta.id)
            ET.SubElement(root, "agencias_id").text = str(conta.agencias_id)
            ET.SubElement(root, "tipo_conta").text = conta.tipo_conta
            
            xml_str = ET.tostring(root)

            return Response(content=xml_str, media_type="application/xml")


@router.put("/{id}")
async def update(id: int, request: Request, db: Session = Depends(get_db)):
    if not ContasService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada!"
        )
    
    content_type = request.headers.get("Content-Type")
    accept = request.headers.get("Accept")

    # Verifica o formato da requisição
    if content_type == "application/json":
        json = await request.json()
        conta = ContasService.save(db, Contas(**json))
         
        root = ET.Element("conta")
        ET.SubElement(root, "id").text = str(conta.id)
        ET.SubElement(root, "agencias_id").text = str(conta.agencias_id)
        ET.SubElement(root, "tipo_conta").text = conta.tipo_conta
        
        xml_str = ET.tostring(root)

        # Verifica o formato da resposta
        if accept == "application/json" or accept == "text/plain" or accept == "*/*" or accept == "application/json, text/plain, */*":
            return ContasResponse.from_orm(conta)
        elif accept == "application/xml" or accept == "text/plain" or accept == "*/*" or accept == "application/xml, text/plain, */*":
            return Response(content=xml_str.decode("utf-8"), media_type="application/xml")

    # Verifica o formato da requisição
    elif content_type == "application/xml":
        xml = await request.body()
        json = xmltodict.parse(xml)
        conta = ContasService.save(db, Contas(**json['contas']))

        # Verifica o formato da resposta
        if accept == "application/json" or accept == "text/plain" or accept == "*/*" or accept == "application/json, text/plain, */*":
            return ContasResponse.from_orm(conta)
        elif accept == "application/xml" or accept == "text/plain" or accept == "*/*" or accept == "application/xml, text/plain, */*":
            return Response(content=conta.to_xml(), media_type="application/xml")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    if not ContasService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada!"
        )
    ContasService.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)