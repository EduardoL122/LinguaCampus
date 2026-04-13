# model/evaluaciones.py
# Funciones de acceso a datos para la tabla 'evaluaciones'.

from config.db import get_connection, close_connection


def obtener_todas():
    """
    Retorna todas las evaluaciones con nombre de estudiante y grupo.
    Usa JOIN para mostrar datos legibles.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT ev.id, ev.modulo, ev.nota,
                   ev.estudiante_id, ev.grupo_id,
                   e.nombre       AS estudiante,
                   g.nombre_grupo AS grupo
            FROM evaluaciones ev
            JOIN estudiantes e ON ev.estudiante_id = e.id
            JOIN grupos      g ON ev.grupo_id      = g.id
            ORDER BY e.nombre, ev.modulo
        """)
        return cursor.fetchall()
    finally:
        close_connection(conn)


def insertar(estudiante_id, grupo_id, modulo, nota): # Inserta una nueva evaluacion para un estudiante en un grupo.
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO evaluaciones (estudiante_id, grupo_id, modulo, nota) "
            "VALUES (%s, %s, %s, %s)",
            (estudiante_id, grupo_id, modulo, nota)
        )
        conn.commit()
    finally:
        close_connection(conn)


def actualizar(id_evaluacion, estudiante_id, grupo_id, modulo, nota): # Actualiza los datos de un evaluacion por su ID.
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE evaluaciones SET estudiante_id=%s, grupo_id=%s, modulo=%s, nota=%s "
            "WHERE id=%s",
            (estudiante_id, grupo_id, modulo, nota, id_evaluacion)
        )
        conn.commit()
    finally:
        close_connection(conn)


def eliminar(id_evaluacion): # elimina una evalucaion por su ID.
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM evaluaciones WHERE id = %s", (id_evaluacion,))
        conn.commit()
    finally:
        close_connection(conn)
