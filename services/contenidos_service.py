from database.connection import ConnectionFactory
from schemas.contenido import ContenidoOut

def obtener_contenidos():
    conn = ConnectionFactory.create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM contenidos"
    )
    rows = cursor.fetchall()
    return [
        ContenidoOut(
            id=row[0],
            titulo=row[1],
            descripcion=row[2],
            fecha_lanzamiento=str(row[3]) if row[3] else None,
            tipo_contenido=row[4],
            imagen=row[5]
        )
        for row in rows
    ]
