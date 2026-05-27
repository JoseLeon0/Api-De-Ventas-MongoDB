from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from typing import List

from database import coleccion_opiniones
from schemas import OpinionCreate, OpinionOut

app = FastAPI(
    title="API Opiniones - Cafetería Orizaba",
    description="API para consultar y gestionar opiniones de clientes.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper para convertir documento Mongo a diccionario
def opinion_serializer(opinion) -> dict:
    return {
        "id": str(opinion["_id"]),
        "cafeteria": opinion["cafeteria"],
        "opinion": opinion["opinion"],
        "sentimiento": opinion["sentimiento"]
    }


# ── Health check ─────────────────────────────────────────
@app.get("/")
async def root():
    return {"mensaje": "API Opiniones Cafetería activa ✅"}


# ── Obtener todas las opiniones ───────────────────────────
@app.get("/opiniones", response_model=List[OpinionOut])
async def get_opiniones():
    opiniones = []
    async for opinion in coleccion_opiniones.find():
        opiniones.append(opinion_serializer(opinion))
    return opiniones


# ── Obtener opinión por ID ────────────────────────────────
@app.get("/opiniones/{id}", response_model=OpinionOut)
async def get_opinion(id: str):
    opinion = await coleccion_opiniones.find_one({"_id": ObjectId(id)})
    if not opinion:
        raise HTTPException(status_code=404, detail="Opinión no encontrada")
    return opinion_serializer(opinion)


# ── Filtrar por cafeteria o sentimiento ──────────────────
@app.get("/opiniones/buscar/filtro")
async def filtrar_opiniones(cafeteria: str = None, sentimiento: str = None):
    filtro = {}
    if cafeteria:
        filtro["cafeteria"] = {"$regex": cafeteria, "$options": "i"}
    if sentimiento:
        filtro["sentimiento"] = {"$regex": sentimiento, "$options": "i"}

    opiniones = []
    async for opinion in coleccion_opiniones.find(filtro):
        opiniones.append(opinion_serializer(opinion))
    return opiniones


# ── Crear una opinión ─────────────────────────────────────
@app.post("/opiniones", response_model=OpinionOut)
async def crear_opinion(opinion: OpinionCreate):
    resultado = await coleccion_opiniones.insert_one(opinion.dict())
    creado = await coleccion_opiniones.find_one({"_id": resultado.inserted_id})
    return opinion_serializer(creado)


# ── Eliminar una opinión ──────────────────────────────────
@app.delete("/opiniones/{id}")
async def eliminar_opinion(id: str):
    resultado = await coleccion_opiniones.delete_one({"_id": ObjectId(id)})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Opinión no encontrada")
    return {"mensaje": "Opinión eliminada ✅"}