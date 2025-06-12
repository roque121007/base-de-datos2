from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# CORS para permitir acceso externo (ej. desde Flutter web o móvil)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Leer los tres archivos Excel al iniciar
def cargar_excel(ruta):
    df = pd.read_excel(ruta)
    df.fillna("", inplace=True)
    return df.to_dict(orient="records")

data1 = cargar_excel("base_de_datos_tutor.xlsx")
data2 = cargar_excel("base_datos_tutorados.xlsx")
data3 = cargar_excel("base_datos_tutor_anterior.xlsx")

# Ruta raíz
@app.get("/")
def read_root():
    return {"message": "API con múltiples archivos Excel"}

# Endpoints para cada archivo
@app.get("/items1/")
def get_items1():
    return data1

@app.get("/items2/")
def get_items2():
    return data2

@app.get("/items3/")
def get_items3():
    return data3

@app.get("/items1/{item_id}")
def get_item1(item_id: int):
    if item_id < 0 or item_id >= len(data1):
        raise HTTPException(status_code=404, detail="Item no encontrado en base 1")
    return data1[item_id]

@app.get("/items2/{item_id}")
def get_item2(item_id: int):
    if item_id < 0 or item_id >= len(data2):
        raise HTTPException(status_code=404, detail="Item no encontrado en base 2")
    return data2[item_id]

@app.get("/items3/{item_id}")
def get_item3(item_id: int):
    if item_id < 0 or item_id >= len(data3):
        raise HTTPException(status_code=404, detail="Item no encontrado en base 3")
    return data3[item_id]
