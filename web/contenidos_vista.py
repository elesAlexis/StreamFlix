from fastapi import APIRouter, Request, Cookie,HTTPException,  status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import  Depends
from typing import Optional
from auth.jwt_handler import verificar_token
import httpx
async def obtener_contenidos(user_api_url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(user_api_url)
            response.raise_for_status() # Lanza una excepción si hay un error HTTP (4xx o 5xx)
            owner_data = response.json()
            return owner_data
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error al obtener usuario via HTTP: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error de red al llamar al endpoint de usuario: {e}"
            )
router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/contenidos_vista")
async def contenidos(request: Request, access_token: Optional[str] = Cookie(None)):

    if not access_token:
        #raise HTTPException(status_code=401, detail="No autorizado")
        return RedirectResponse(url='/login')
    
    # Remover "Bearer " del token
    token = access_token.replace("Bearer ", "") if access_token.startswith("Bearer ") else access_token
    
    payload = verificar_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")

    user_api_url = f"{request.base_url}contenidos"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(user_api_url)
            response.raise_for_status() # Lanza una excepción si hay un error HTTP (4xx o 5xx)
            owner_data = response.json()
            print(owner_data)
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error al obtener usuario via HTTP: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error de red al llamar al endpoint de usuario: {e}"
            )
    owner_data = await obtener_contenidos(user_api_url)
    peliculas = [c for c in owner_data if c["tipo_contenido"] == "pelicula"]
    # print(peliculas[1]['imagen'])
    series = [c for c in owner_data if c["tipo_contenido"] == "serie"]
    # Aquí puedes obtener los datos de los contenidos desde la base de datos o cualquier otra fuente
    # Por ahora, simplemente pasaremos una lista vacía
       

    
    return  templates.TemplateResponse("ver_contenidos.html", {
        "request": request,
        "title": "StreamFlix - Tu plataforma de contenido",
        ##"contenidos": contenidos,
        ##'populares': owner_data,
        'peliculas': peliculas,
        'series': series,
        'usuario': payload.get('nombre')
    })

@router.get("/series")
async def series(request: Request, access_token: Optional[str] = Cookie(None)):
    if not access_token:
        #raise HTTPException(status_code=401, detail="No autorizado")
        return RedirectResponse(url='/login')
    
    # Remover "Bearer " del token
    token = access_token.replace("Bearer ", "") if access_token.startswith("Bearer ") else access_token
    
    payload = verificar_token(token)
    print(payload)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")
    user_api_url = f"{request.base_url}contenidos"
    contenidos = await obtener_contenidos(user_api_url)
    
    series = [c for c in contenidos if c["tipo_contenido"] == "serie"]
   
    return  templates.TemplateResponse("ver_contenidos.html", {
        "request": request,
        "title": "StreamFlix - Tu plataforma de contenido",
        ##"contenidos": contenidos,
        # 'populares': populares,
        # 'peliculas': peliculas,
        'series': series
    })


@router.get("/peliculas")
async def peliculas(request: Request,  access_token: Optional[str] = Cookie(None)):
    
    if not access_token:
        #raise HTTPException(status_code=401, detail="No autorizado")
        return RedirectResponse(url='/login')
    
    # Remover "Bearer " del token
    token = access_token.replace("Bearer ", "") if access_token.startswith("Bearer ") else access_token
    
    payload = verificar_token(token)
    print(payload)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")
    user_api_url = f"{request.base_url}contenidos"
    contenidos = await obtener_contenidos(user_api_url)
    
    peliculas = [c for c in contenidos if c["tipo_contenido"] == "pelicula"]
    # print(request.json())
    return  templates.TemplateResponse("ver_contenidos.html", {
        "request": request,
        "title": "StreamFlix - Tu plataforma de contenido",
        ##"contenidos": contenidos,
        # 'populares': populares,
        'peliculas': peliculas,
        # 'series': series
    })

