# model/inscripciones.py
# Funciones de acceso a datos para la tabla 'inscripciones'.
# Tabla intermedia de la relacion muchos a muchos entre estudiantes y grupos.

from config.db import get_connection, close_connection
from model.grupos import obtener_cupo


def obtener_todas():
    """
    Retorna todas las inscripciones con datos del estudiante,
    grupo, idioma y nivel usando JOIN.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT ins.id, ins.fecha_inscripcion, ins.estado,
                   ins.estudiante_id, ins.grupo_id,
                   e.nombre          AS estudiante,
                   g.nombre_grupo    AS grupo,
                   i.nombre_idioma   AS idioma,
                   n.nombre          AS nivel
            FROM inscripciones ins
            JOIN estudiantes e ON ins.estudiante_id = e.id
            JOIN grupos      g ON ins.grupo_id      = g.id
            JOIN idiomas     i ON g.idioma_id       = i.id
            JOIN niveles     n ON g.nivel_id        = n.id
            ORDER BY ins.fecha_inscripcion DESC
        """)
        return cursor.fetchall()
    finally:
        close_connection(conn)


def insertar(estudiante_id, grupo_id, fecha, estado):
    """
    Inscribe a un estudiante en un grupo.
    Verifica: cupo disponible y que no este ya inscrito activo.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()

        # Regla: verificar cupo disponible
        cupo_max, inscritos = obtener_cupo(grupo_id)
        if inscritos >= cupo_max:
            raise ValueError(
                f"Cupo lleno. El grupo permite maximo {cupo_max} estudiantes."
            )

        # Regla: no duplicar inscripcion activa
        cursor.execute(
            "SELECT COUNT(*) FROM inscripciones "
            "WHERE estudiante_id = %s AND grupo_id = %s AND estado = 'activo'",
            (estudiante_id, grupo_id)
        )
        if cursor.fetchone()[0] > 0:
            raise ValueError("El estudiante ya esta inscrito activo en este grupo.")

        cursor.execute(
            "INSERT INTO inscripciones (estudiante_id, grupo_id, fecha_inscripcion, estado) "
            "VALUES (%s, %s, %s, %s)",
            (estudiante_id, grupo_id, fecha, estado)
        )
        conn.commit()
    finally:
        close_connection(conn)


def actualizar(id_inscripcion, estudiante_id, grupo_id, fecha, estado): # Actualiza los datos de una inscripcion por su ID. 
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE inscripciones SET estudiante_id=%s, grupo_id=%s, "
            "fecha_inscripcion=%s, estado=%s WHERE id=%s",
            (estudiante_id, grupo_id, fecha, estado, id_inscripcion)
        )
        conn.commit()
    finally:
        close_connection(conn)


def eliminar(id_inscripcion): # Elimina una inscripcion por su ID.
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inscripciones WHERE id = %s", (id_inscripcion,))
        conn.commit()
    finally:
        close_connection(conn)
