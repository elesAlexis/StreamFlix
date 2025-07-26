# 🎬 Proyecto Netflix con FastAPI

## ⚙️ Instalación y Configuración

```bash
# 1. Clonar el repositorio
git clone https://github.com/cmestradap/curso_fast_api
cd curso_fast_api

# 2. Crear entorno virtual
python -m venv fast_api_venv

# 3. Activar entorno virtual
# En Windows:
.\venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables de entorno
# Crear un archivo .env con el siguiente contenido:
# DATABASE_URL=SQL Server://usuario:password@localhost/netflix_db
# SECRET_KEY=tu_clave_secreta
# DEBUG=True

o

#SERVER=10.200.14.102
#DATABASE=
#USERNAME=
#PASSWORD=
#DB_AUTH_MODE=windows 

# 6. Ejecutar la aplicación
uvicorn app.main:app --reload
