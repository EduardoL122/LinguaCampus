# model/docentes.py
# Funciones de acceso a datos para la tabla 'docentes'.

from config.db import get_connection, close_connection


def obtener_todos():
    """
    Retorna todos los docentes con el nombre del idioma principal.
    Usa LEFT JOIN con idiomas.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT d.id, d.nombre, d.idioma_id, d.nivel_certificado, d.estado,
            IFNULL(i.nombre_idioma, 'Sin idioma') AS idioma
            FROM docentes d
            LEFT JOIN idiomas i ON d.idioma_id = i.id
            ORDER BY d.nombre
        """)
        return cursor.fetchall()
    finally:
        close_connection(conn)


def insertar(nombre, idioma_id, nivel_certificado, estado): # Inserta un nuevo docente en la base de datos.
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO docentes (nombre, idioma_id, nivel_certificado, estado) VALUES (%s, %s, %s, %s)",
            (nombre, idioma_id, nivel_certificado, estado)
        )
        conn.commit()
    finally:
        close_connection(conn)


def actualizar(id_docente, nombre, idioma_id, nivel_certificado, estado): # Actualiza los datos de un docente por su ID.
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE docentes SET nombre=%s, idioma_id=%s, nivel_certificado=%s, estado=%s WHERE id=%s",
            (nombre, idioma_id, nivel_certificado, estado, id_docente)
        )
        conn.commit()
    finally:
        close_connection(conn)


def eliminar(id_docente):
    """
    Elimina un docente si no tiene grupos asignados.
    Lanza ValueError si hay grupos dependientes.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM grupos WHERE docente_id = %s",
            (id_docente,)
        )
        if cursor.fetchone()[0] > 0:
            raise ValueError("No se puede eliminar: el docente tiene grupos asignados.")
        cursor.execute("DELETE FROM docentes WHERE id = %s", (id_docente,))
        conn.commit()
    finally:
        close_connection(conn)
