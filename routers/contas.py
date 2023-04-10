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
def list(request: Request, db: Session = Depends(get_db)):
    contas = ContasService.list(db)
    response_obj = [ContasResponse.from_orm(conta) for conta in contas]

    root = ET.Element("contas")
    for conta in response_obj:
        conta_elem = ET.SubElement(root, "conta")
        ET.SubElement(conta_elem, "id").text = str(conta.id)
        ET.SubElement(conta_elem, "agencias_id").text = str(conta.agencias_id)
        ET.SubElement(conta_elem, "tipo_conta").text = conta.tipo_conta
        
        xml_str = ET.tostring(root)

    # Verifica o formato da resposta
    accept = request.headers.get("Accept")
    if accept == "application/json":
        return [ContasResponse.from_orm(conta) for conta in contas]
    elif accept == "application/xml":    
        return Response(content=xml_str, media_type="application/xml")


@router.get("/{id}", response_model=ContasResponse)
def find_id(request: Request, id: int, db: Session = Depends(get_db)):
    conta = ContasService.get_id(db, id)
    if not conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada!"
        )
    
    root = ET.Element("agencia")
    ET.SubElement(root, "id").text = str(conta.id)
    ET.SubElement(root, "agencias_id").text = str(conta.agencias_id)
    ET.SubElement(root, "tipo_conta").text = conta.tipo_conta
    
    xml_str = ET.tostring(root)

    # Verifica o formato da resposta
    accept = request.headers.get("Accept")
    if accept == "application/json":
        return ContasResponse.from_orm(conta)
    elif accept == "application/xml":    
        return Response(content=xml_str, media_type="application/xml")


@router.post("", response_model=ContasResponse, status_code=status.HTTP_201_CREATED)
async def create(request: Request, db: Session = Depends(get_db)):
    content_type = request.headers.get("Content-Type")
    accept = request.headers.get("Accept")
    
    # Verifica o formato da requisição
    if content_type == "application/json":
        json = await request.json()
        conta = ContasService.save(db, Contas(**json))
        # Verifica o formato da resposta
        if accept == "application/json":
            return ContasResponse.from_orm(conta)
        elif accept == "application/xml":    
            return Response(content=xml_str, media_type="application/xml")
    elif content_type == "application/xml":
        xml = await request.body()
        json = xmltodict.parse(xml)
        conta = ContasService.save(db, Contas(**json['contas']))
         
        root = ET.Element("agencia")
        ET.SubElement(root, "id").text = str(conta.id)
        ET.SubElement(root, "agencias_id").text = str(conta.agencias_id)
        ET.SubElement(root, "tipo_conta").text = conta.tipo_conta
        
        xml_str = ET.tostring(root)
        # Verifica o formato da resposta
        if accept == "application/json":
            return ContasResponse.from_orm(conta)
        elif accept == "application/xml":    
            return Response(content=xml_str, media_type="application/xml")


@router.put("/{id}", response_model=ContasResponse)
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
         
        root = ET.Element("agencia")
        ET.SubElement(root, "id").text = str(conta.id)
        ET.SubElement(root, "agencias_id").text = str(conta.agencias_id)
        ET.SubElement(root, "tipo_conta").text = conta.tipo_conta
        
        xml_str = ET.tostring(root)

        # Verifica o formato da resposta
        if accept == "application/json":
            return ContasResponse.from_orm(conta)
        elif accept == "application/xml":    
            return Response(content=xml_str, media_type="application/xml")
    elif content_type == "application/xml":
        xml = await request.body()
        json = xmltodict.parse(xml)
        conta = ContasService.save(db, Contas(**json['contas']))
        # Verifica o formato da resposta
        if accept == "application/json":
            return ContasResponse.from_orm(conta)
        elif accept == "application/xml":    
            return Response(content=conta.to_xml(), media_type="application/xml")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    if not ContasService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada!"
        )
    ContasService.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
