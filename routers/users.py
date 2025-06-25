from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas.user import User
from services.usuarios_service import obtener_usuarios

router = APIRouter()

@router.get("/usuarios", response_model=List[User])
async def listar_usuarios(skip: int = 0, limit: int = 100):
    return obtener_usuarios(skip=skip, limit=limit)