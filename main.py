from fastapi import FastAPI, APIRouter

app = FastAPI()
# router = APIRouter()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# app.include_router(prefix='/read_root', router=router)