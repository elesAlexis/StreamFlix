from fastapi import APIRouter
from typing import List
from schemas.user import UserCreate, UserResponse
from services.usuarios_service import obtener_usuarios, crear_usuario

router = APIRouter()

@router.get("/usuarios", response_model=List[UserResponse])
async def listar_usuarios(skip: int = 0, limit: int = 100):
    return obtener_usuarios(skip=skip, limit=limit)

@router.post("/usuarios", response_model=UserResponse, status_code=201)
async def crear(usuario: UserCreate):
    return crear_usuario(usuario)