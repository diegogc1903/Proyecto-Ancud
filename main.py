import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Literal



@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Equivalente a "startup": se ejecuta al iniciar
    print("La aplicación se está iniciando...")
    
    yield # Aquí el servidor se pausa, está activo y recibiendo tráfico de internet
    
    # 2. Equivalente a "shutdown": se ejecuta al apagar (ej. Ctrl+C en la terminal)
    print("La aplicación se está apagando...")

# Conectas la función a tu app al momento de crearla.
app = FastAPI(lifespan=lifespan)

# Configuración del Middleware CORS (Analiza la petición de wordpress antes de ser recibida)
app.add_middleware(
    CORSMiddleware,
    # Reemplaza esta URL por el dominio real de tu WordPress
    allow_origins=["http://127.0.0.1:5500", "http://localhost:8000"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.get('/') #PRUEBA EN RAIZ
async def read_root():
    return {"mensaje": "¡Hola, FastAPI!"}
  
# VALIDACIÓN DE DATOS CON PYDANTIC

class RegistroLocal(BaseModel):
    nombre_dueno: str
    correo: str
    nombre_local: str
    rut: int
    categoria: Literal["Restaurante", "Cafetería", "Hospedaje", "Atracción", "Tour"] #Solo permitir estos datos en especifico. EJ: No permite que se ingrese como categoría "Selecciona una categoría...".
    telefono: int
    direccion: str

@app.post('/users-register/')
async def create_item(datos: RegistroLocal):
    archivo = "locales_registrados.json"
    lista_locales = []
    
    # 1. Leer el archivo si ya existe
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            try:
                lista_locales = json.load(f)
            except json.JSONDecodeError:
                pass
                
    # 2. Agregar el nuevo dato validado a la lista
    lista_locales.append(datos.model_dump())
    
    # 3. Sobrescribir el archivo JSON
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(lista_locales, f, indent=4, ensure_ascii=False)
        
    return {"mensaje": f"Local '{datos.nombre_local}' registrado exitosamente"}