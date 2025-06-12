from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# CORS para permitir acceso externo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Leer Excel al iniciar
df = pd.read_excel("base_de_datos.xlsx")
df.fillna("", inplace=True)
data = df.to_dict(orient="records")

@app.get("/")
def read_root():
    return {"message": "API desde Excel en Render"}

@app.get("/items/")
def get_items():
    return data

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id < 0 or item_id >= len(data):
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return data[item_id]
