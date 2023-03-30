from fastapi import FastAPI
from database.connection import engine, Base
from routers.cidades import router as cidades_router
from routers.agencias import router as agencias_router
from routers.contas import router as contas_router
from routers.clientes import router as clientes_router
from routers.clientes_has_contas import router as clientes_has_contas_router
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World"}

app.include_router(cidades_router, prefix="/cidades")
app.include_router(agencias_router, prefix="/agencias")
app.include_router(contas_router, prefix="/contas")
app.include_router(clientes_router, prefix="/clientes")
app.include_router(clientes_has_contas_router, prefix="/clientes_has_contas")