
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/register")
async def register(request: Request):
    print (request.json())
    return templates.TemplateResponse("auth/creacion_usuario.html", {
        "request": request,
        "title": "Iniciar Sesión"
    })