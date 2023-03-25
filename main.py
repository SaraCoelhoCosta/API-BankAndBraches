from fastapi import FastAPI
from database.connection import engine, Base
from routers.cidades import router as cidades_router
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World"}

app.include_router(cidades_router, prefix="/cidades")

