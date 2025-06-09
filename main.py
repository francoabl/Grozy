from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from scraping.db import SessionLocal, Producto as DBProducto  # <-- Importa tu modelo y sesión
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estructura del Producto para la API
class Producto(BaseModel):
    id: int
    nombre: str
    precio: float
    enlace: str
    supermercado: str
    imagen_url: str

# Función para obtener productos desde la base de datos
def get_productos_db():
    db = SessionLocal()
    productos = db.query(DBProducto).all()
    resultado = [
        Producto(
            id=p.id,
            nombre=p.nombre,
            precio=p.precio,
            enlace=p.enlace,
            supermercado=p.supermercado,
            imagen_url=p.imagen_url
        ) for p in productos
    ]
    db.close()
    return resultado

@app.get("/productos", response_model=List[Producto])
def obtener_productos():
    return get_productos_db()

@app.get("/productos/{producto_id}", response_model=Producto)
def obtener_producto(producto_id: int):
    db = SessionLocal()
    producto = db.query(DBProducto).filter(DBProducto.id == producto_id).first()
    db.close()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return Producto(
        id=producto.id,
        nombre=producto.nombre,
        precio=producto.precio,
        enlace=producto.enlace,
        supermercado=producto.supermercado,
        imagen_url=producto.imagen_url
    )
