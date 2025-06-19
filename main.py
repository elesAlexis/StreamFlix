# app/main.py - Primera aplicación FastAPI
from fastapi import FastAPI
from pydantic import BaseModel
from routers import contenidos

# Crear la aplicación FastAPI
app = FastAPI(
    title="Netflix API",
    description="API Backend para plataforma tipo Netflix",
    version="1.0.0"
)

app.include_router(contenidos.router)

# Endpoint principal
@app.get("/")
async def root():
    return {
        "mensaje": "¡Bienvenido a Netflix API!",
        "estado": "online",
        "version": "1.0.0",
        "documentacion": "/docs"
    }


@app.get("/peliculas")
async def listar_peliculas():
    return {
        "peliculas": [
            {"id": 1, "titulo": "El Padrino", "año": 1972},
            {"id": 2, "titulo": "Pulp Fiction", "año": 1994}
        ]
    }

@app.get("/series")
async def listar_series():
    return {
        "series": [
            {"id": 1, "titulo": "Stranger Things", "temporadas": 4},
            {"id": 2, "titulo": "The Crown", "temporadas": 6}
        ]
    }

