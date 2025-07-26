from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from services.usuarios_service import autenticar_usuario, verificar_existencia_usuario
from auth.jwt_handler import crear_token

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login")
async def login_form(request: Request):
    return templates.TemplateResponse("auth/login.html", {
        "request": request,
        "title": "Iniciar Sesión"
    })

@router.post("/web/login")
async def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    try:
        # Reutilizar tu servicio existente
        usuario = autenticar_usuario(email, password)
        
        
        if not usuario:
            return templates.TemplateResponse("auth/login.html", {
                "request": request,
                "title": "Iniciar Sesión",
                "error": "Credenciales inválidas",
                "email": email  # Mantener email en el form
            })
        
        # Crear token usando tu función existente
        token = crear_token({"nombre": str(usuario.get("username")), "rol": usuario.get("rol")})
        
        # Redirigir a contenidos
        response = RedirectResponse(url="/contenidos_vista", status_code=302)
        response.set_cookie(
            key="access_token", 
            value=f"Bearer {token}",
            httponly=True,
            max_age=1800  # 30 minutos

        )
        return response
        
    except Exception as e:
        return templates.TemplateResponse("auth/login.html", {
            "request": request,
            "title": "Iniciar Sesión",
            "error": "Error interno del servidor",
            "email": email
        })

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")
    return response

@router.post("/web/crear_usuario")
async def login_submit(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    password_2: str = Form(...)):
    

    #verificar contraseña
    if password != password_2:
        return templates.TemplateResponse("auth/crear_usuario.html", {
            "request": request,
            "title": "Crear Usuario",
            "error": "Las contraseñas no coinciden",
            "email": email
        })
    
    #verificar que el usuario no exista
    usuario = verificar_existencia_usuario(email)
    if usuario:
        return templates.TemplateResponse("auth/crear_usuario.html", {
            "request": request,
            "title": "Crear Usuario",
            "error": "El usuario ya existe",
            "email": email
        })

    #guardamos usuairo
    from services.usuarios_service import crear_usuario
    from schemas.user import UserCreate
    
    usuario_crear = UserCreate(nombre=nombre, email=email, contrasena=password)
    usuario_creado = crear_usuario(usuario_crear)
    #redirigir a login
    return templates.TemplateResponse("auth/login.html", {
        "request": request,
        "title": "Iniciar Sesión",
        "exito": "Usuario creado correctamente",
        "email": email
    })
    