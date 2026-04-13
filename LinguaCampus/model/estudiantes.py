# model/estudiantes.py
# Funciones de acceso a datos para la tabla 'estudiantes'.

from config.db import get_connection, close_connection


def obtener_todos(): # Retorna todos los estudiantes ordenados por nombre.
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM estudiantes ORDER BY nombre")
        return cursor.fetchall()
    finally:
        close_connection(conn)


def insertar(nombre, email, estado): # Inserta un nuevo estudiante a la base de datos.
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO estudiantes (nombre, email, estado) VALUES (%s, %s, %s)",
            (nombre, email, estado)
        )
        conn.commit()
    finally:
        close_connection(conn)


def actualizar(id_estudiante, nombre, email, estado): # Actualiza los datos de un estudiante por su ID.
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE estudiantes SET nombre=%s, email=%s, estado=%s WHERE id=%s",
            (nombre, email, estado, id_estudiante)
        )
        conn.commit()
    finally:
        close_connection(conn)


def eliminar(id_estudiante):
    """
    Elimina un estudiante si no tiene inscripciones registradas.
    Lanza ValueError si hay dependencias.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM inscripciones WHERE estudiante_id = %s",
            (id_estudiante,)
        )
        if cursor.fetchone()[0] > 0:
            raise ValueError("No se puede eliminar: el estudiante tiene inscripciones.")
        cursor.execute("DELETE FROM estudiantes WHERE id = %s", (id_estudiante,))
        conn.commit()
    finally:
        close_connection(conn)
