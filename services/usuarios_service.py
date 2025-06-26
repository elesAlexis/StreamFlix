from database.connection import ConnectionFactory
from schemas.user import UserResponse, UserCreate


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
        UserResponse(
            id=row[0],
            nombre=row[1],
            email=row[2],
        )
        for row in rows
    ]


def crear_usuario(usuario: UserCreate) -> UserResponse:
    conn = ConnectionFactory.create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO usuarios (nombre, email, contrasena)
        OUTPUT INSERTED.id, INSERTED.nombre, INSERTED.email
        VALUES (?, ?, ?)
    """, (usuario.nombre, usuario.email, usuario.contrasena))

    row = cursor.fetchone()
    conn.commit()
    cursor.close()

    return UserResponse(
        id=row.id,
        nombre=row.nombre,
        email=row.email
    )