# model/niveles.py
# Funciones de acceso a datos para la tabla 'niveles'.

from config.db import get_connection, close_connection


def obtener_todos():
    """
    Retorna todos los niveles con el nombre del idioma asociado.
    Usa LEFT JOIN para incluir niveles sin idioma asignado.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT n.id, n.nombre, n.idioma_id,
                   IFNULL(i.nombre_idioma, 'Sin idioma') AS idioma
            FROM niveles n
            LEFT JOIN idiomas i ON n.idioma_id = i.id
            ORDER BY n.nombre
        """)
        return cursor.fetchall()
    finally:
        close_connection(conn)


def insertar(nombre, idioma_id): # Inserta un nuevo nivel, idioma_id puede ser None.
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO niveles (nombre, idioma_id) VALUES (%s, %s)",
            (nombre, idioma_id)
        )
        conn.commit()
    finally:
        close_connection(conn)


def actualizar(id_nivel, nombre, idioma_id): # Actualiza el nombre e idioma de un nivel por su ID.
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE niveles SET nombre = %s, idioma_id = %s WHERE id = %s",
            (nombre, idioma_id, id_nivel)
        )
        conn.commit()
    finally:
        close_connection(conn)


def eliminar(id_nivel):
    """
    Elimina un nivel si no esta asignado a ningun grupo.
    Lanza ValueError si hay dependencias.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM grupos WHERE nivel_id = %s",
            (id_nivel,)
        )
        if cursor.fetchone()[0] > 0:
            raise ValueError("No se puede eliminar: el nivel esta asignado a un grupo.")
        cursor.execute("DELETE FROM niveles WHERE id = %s", (id_nivel,))
        conn.commit()
    finally:
        close_connection(conn)
