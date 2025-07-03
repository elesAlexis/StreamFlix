from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from routers import contenidos, users
from auth import auth

# Crear la aplicación FastAPI
app = FastAPI(
    title="Netflix API",
    description="API Backend para plataforma tipo Netflix",
    version="1.0.0"
)

# Definir esquema de seguridad para Swagger UI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Demo JWT",
        version="1.0.0",
        description="API con JWT y rutas protegidas",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"bearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(contenidos.router)
app.include_router(users.router)
app.include_router(auth.router)

# Endpoint principal
@app.get("/")
async def root():
    return {
        "mensaje": "¡Bienvenido a Netflix API!",
        "estado": "online",
        "version": "1.0.0",
        "documentacion": "/docs"
    }


