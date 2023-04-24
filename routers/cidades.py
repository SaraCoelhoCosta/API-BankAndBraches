from sqlalchemy.orm import Session
from database.models import Cidades
from services.cidadesServices import CidadesService
from schemas.schema_cidades import CidadesResponse
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
import xml.etree.ElementTree as ET
import xmltodict
from database.connection import get_db

router = APIRouter()


@router.get("", response_model=list[CidadesResponse])
def list(request: Request, db: Session = Depends(get_db)):
    
    cidades = CidadesService.list(db)

    # Verifica o formato da resposta
    accept = request.headers.get("Accept")
    if accept == "application/json":
        return cidades
    elif accept == "application/xml":    
        response_obj = [CidadesResponse.from_orm(cidade) for cidade in cidades]

        root = ET.Element("cidades")
        for cidade in response_obj:
            cidade_elem = ET.SubElement(root, "cidade")
            ET.SubElement(cidade_elem, "id").text = str(cidade.id)
            ET.SubElement(cidade_elem, "nome").text = cidade.nome
        
        xml_str = ET.tostring(root)
        return Response(content=xml_str, media_type="application/xml")


@router.get("/{id}", response_model=CidadesResponse)
def find_id(request: Request, id: int, db: Session = Depends(get_db)):
    cidade = CidadesService.get_id(db, id)
    if not cidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cidade não encontrada!"
        )
    
    root = ET.Element("cidade")
    ET.SubElement(root, "id").text = str(cidade.id)
    ET.SubElement(root, "nome").text = cidade.nome
    
    xml_str = ET.tostring(root)

    # Verifica o formato da resposta
    accept = request.headers.get("Accept")
    if accept == "application/json":
        return CidadesResponse.from_orm(cidade)
    elif accept == "application/xml":    
        return Response(content=xml_str, media_type="application/xml")


@router.post("", response_model=CidadesResponse, status_code=status.HTTP_201_CREATED)
async def create(request: Request, db: Session = Depends(get_db)):
    content_type = request.headers.get("Content-Type")
    accept = request.headers.get("Accept")
    
    # Verifica o formato da requisição
    if content_type == "application/json":
        json = await request.json()
        cidade = CidadesService.save(db, Cidades(**json))
        # Verifica o formato da resposta
        if accept == "application/json":
            return CidadesResponse.from_orm(cidade)
        elif accept == "application/xml":    
            return Response(content=xml_str, media_type="application/xml")
    elif content_type == "application/xml":
        xml = await request.body()
        json = xmltodict.parse(xml)
        cidade = CidadesService.save(db, Cidades(**json['cidades'])) 

        root = ET.Element("cidade")
        ET.SubElement(root, "id").text = str(cidade.id)
        ET.SubElement(root, "nome").text = cidade.nome
        
        xml_str = ET.tostring(root)
        
        # Verifica o formato da resposta
        if accept == "application/json":
            return CidadesResponse.from_orm(cidade)
        elif accept == "application/xml":    
            return Response(content=xml_str, media_type="application/xml")


@router.put("/{id}", response_model=CidadesResponse)
async def update(id: int, request: Request, db: Session = Depends(get_db)):
    if not CidadesService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cidade não encontrada!"
        )
    content_type = request.headers.get("Content-Type")
    accept = request.headers.get("Accept")
    
    # Verifica o formato da requisição
    if content_type == "application/json":
        json = await request.json()
        cidade = CidadesService.save(db, Cidades(**json))
        
        root = ET.Element("cidade")
        ET.SubElement(root, "id").text = str(cidade.id)
        ET.SubElement(root, "nome").text = cidade.nome
        
        xml_str = ET.tostring(root)
        
        # Verifica o formato da resposta
        if accept == "application/json":
            return CidadesResponse.from_orm(cidade)
        elif accept == "application/xml":    
            return Response(content=xml_str.decode("utf-8"), media_type="application/xml")
    
    elif content_type == "application/xml":
        xml = await request.body()
        json = xmltodict.parse(xml)
        cidade = CidadesService.save(db, Cidades(**json['cidades']))

        # Verifica o formato da resposta
        if accept == "application/json":
            return CidadesResponse.from_orm(cidade)
        elif accept == "application/xml":    
            return Response(content=cidade.to_xml(), media_type="application/xml")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    if not CidadesService.exists_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cidade não encontrada!"
        )
    CidadesService.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
