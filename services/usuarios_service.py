from database.connection import ConnectionFactory
from schemas.user import User


def obtener_usuarios(skip: int = 0, limit: int = 100):
    conn = ConnectionFactory.create_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
                    SELECT id, nombre, email
                    FROM usuarios
                    ORDER BY id
                    OFFSET ? ROWS
                    FETCH NEXT ? ROWS ONLY
                    """,
        (skip, limit),
    )
    rows = cursor.fetchall()
    return [
        User(
            id=row[0],
            nombre=row[1],
            email=row[2],
        )
        for row in rows
    ]
