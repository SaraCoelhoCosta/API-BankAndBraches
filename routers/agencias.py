from sqlalchemy.orm import Session
from database.models import Agencias
from services.agenciasServices import AgenciasService
from schemas.schema_agencias import AgenciasResponse
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
import xml.etree.ElementTree as ET
import xmltodict
from database.connection import get_db

router = APIRouter()


@router.get("")
def list(request: Request, db: Session = Depends(get_db)):
    agencias = AgenciasService.list(db)

    # Verifica o formato da resposta
    accept = request.headers.get("Accept")
    if accept == "application/json"or accept == "text/plain" or accept == "*/*" or accept == "application/json, text/plain, */*":
        return [AgenciasResponse.from_orm(agencia) for agencia in agencias]
    elif accept == "application/xml" or accept == "text/plain" or accept == "*/*" or accept == "application/xml, text/plain, */*":
        response_obj = [AgenciasResponse.from_orm(agencia) for agencia in agencias]
        
        root = ET.Element("agencias")
        for agencia in response_obj:
            agencia_elem = ET.SubElement(root, "agencia")
            ET.SubElement(agencia_elem, "id").text = str(agencia.id)
            ET.SubElement(agencia_elem, "descricao").text = agencia.descricao
            ET.SubElement(agencia_elem, "sede").text = agencia.sede
            ET.SubElement(agencia_elem, "cidades_id").text = str(agencia.cidades_id)
            
        xml_str = ET.tostring(root)    
        return Response(content=xml_str, media_type="application/xml")


@router.get("/{id}")
def find_id(request: Request, id: int, db: Session = Depends(get_db)):
    
    agencia = AgenciasService.get_id(db, id)
    if not agencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agência não encontrada!"
        )
    
    # Verifica o formato da resposta
    accept = request.headers.get("Accept")
    if accept == "application/json" or accept == "text/plain" or accept == "*/*" or accept == "application/json, text/plain, */*": 
        return AgenciasResponse.from_orm(agencia)
    
    elif accept == "application/xml" or accept == "text/plain" or accept == "*/*" or accept == "application/xml, text/plain, */*":   
        response_obj = AgenciasResponse.from_orm(agencia)

        root = ET.Element("agencia")
        ET.SubElement(root, "id").text = str(agencia.id)
        ET.SubElement(root, "descricao").text = agencia.descricao
        ET.SubElement(root, "sede").text = agencia.sede
        ET.SubElement(root, "cidades_id").text = str(agencia.cidades_id)
    
        xml_str = ET.tostring(root)
        return Response(content=xml_str, media_type="application/xml")


@router.post("")
async def create(request: Request, db: Session = Depends(get_db)):
    content_type = request.headers.get("Content-Type")
    accept = request.headers.get("Accept")
    
    # Verifica o formato da requisição
    if content_type == "application/json":
        json = await request.json()
        agencia = AgenciasService.save(db, Agencias(**json))

        # Verifica o formato da resposta
        if accept == "application/json" or accept == "text/plain" or accept == "*/*" or accept == "application/json, text/plain, */*":
            return AgenciasResponse.from_orm(agencia).json()
        
        elif accept == "application/xml" or accept == "text/plain" or accept == "*/*" or accept == "application/xml, text/plain, */*":    
            xml = await request.body()
            json = xmltodict.parse(xml)
            agencia = AgenciasService.save(db, Agencias(**json['agencias']))
            
            root = ET.Element("agencia")
            ET.SubElement(root, "id").text = str(agencia.id)
            ET.SubElement(root, "descricao").text = agencia.descricao
            ET.SubElement(root, "sede").text = agencia.sede
            ET.SubElement(root, "cidades_id").text = str(agencia.cidades_id)
            
            xml_str = ET.tostring(root)
            
            return Response(content=xml_str, media_type="application/xml")
    
    # Verifica formato da requisição
    elif content_type == "application/xml":
        # Verifica o formato da resposta
        if accept == "application/json" or accept == "text/plain" or accept == "*/*" or accept == "application/json, text/plain, */*":
            return AgenciasResponse.from_orm(agencia)
        
        elif accept == "application/xml" or accept == "text/plain" or accept == "*/*" or accept == "application/xml, text/plain, */*": 
            xml = await request.body()
            json = xmltodict.parse(xml)
            agencia = AgenciasService.save(db, Agencias(**json['agencias']))
            
            root = ET.Element("agencia")
            ET.SubElement(root, "id").text = str(agencia.id)
            ET.SubElement(root, "descricao").text = agencia.descricao
            ET.SubElement(root, "sede").text = agencia.sede
            ET.SubElement(root, "cidades_id").text = str(agencia.cidades_id)
            
            xml_str = ET.tostring(root)  
            return Response(content=xml_str, media_type="application/xml")


@router.put("/{id}")
async def update(id: int, request: Request, db: Session = Depends(get_db)):
    if not AgenciasService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agência não encontrada!"
        )
    content_type = request.headers.get("Content-Type")
    accept = request.headers.get("Accept")
    
    # Verifica o formato da requisição
    if content_type == "application/json":
        json = await request.json()
        agencia = AgenciasService.save(db, Agencias(**json))
        
        root = ET.Element("agencia")
        ET.SubElement(root, "id").text = str(agencia.id)
        ET.SubElement(root, "descricao").text = agencia.descricao
        ET.SubElement(root, "sede").text = agencia.sede
        ET.SubElement(root, "cidades_id").text = str(agencia.cidades_id)
        
        xml_str = ET.tostring(root)

        # Verifica o formato da resposta
        if accept == "application/json" or accept == "text/plain" or accept == "*/*" or accept == "application/json, text/plain, */*":
            return AgenciasResponse.from_orm(agencia)
        elif accept == "application/xml" or accept == "text/plain" or accept == "*/*" or accept == "application/xml, text/plain, */*":    
            return Response(content=xml_str.decode("utf-8"), media_type="application/xml")
   
    # Verifica o formato da requisição     
    elif content_type == "application/xml":
        xml = await request.body()
        json = xmltodict.parse(xml)
        agencia = AgenciasService.save(db, Agencias(**json['agencias']))

        # Verifica o formato da resposta
        if accept == "application/json" or accept == "text/plain" or accept == "*/*" or accept == "application/json, text/plain, */*":
            return AgenciasResponse.from_orm(agencia)
        elif accept == "application/xml" or accept == "text/plain" or accept == "*/*" or accept == "application/xml, text/plain, */*":    
            return Response(content=agencia.to_xml(), media_type="application/xml")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    if not AgenciasService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agência não encontrada!"
        )
    AgenciasService.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
