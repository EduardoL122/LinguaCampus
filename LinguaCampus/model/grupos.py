# model/grupos.py
# Funciones de acceso a datos para la tabla 'grupos'.

from config.db import get_connection, close_connection


def obtener_todos():
    """
    Retorna todos los grupos con nombre de idioma, nivel y docente.
    Usa JOIN con las tres tablas relacionadas.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT g.id, g.nombre_grupo, g.horario, g.cupo_maximo,
                   g.idioma_id, g.nivel_id, g.docente_id,
                   i.nombre_idioma AS idioma,
                   n.nombre        AS nivel,
                   d.nombre        AS docente
            FROM grupos g
            LEFT JOIN idiomas  i ON g.idioma_id  = i.id
            LEFT JOIN niveles  n ON g.nivel_id   = n.id
            LEFT JOIN docentes d ON g.docente_id = d.id
            ORDER BY g.nombre_grupo
        """)
        return cursor.fetchall()
    finally:
        close_connection(conn)


def obtener_cupo(grupo_id):
    """
    Retorna (cupo_maximo, estudiantes_inscritos_activos) de un grupo.
    Se usa para validar el cupo antes de inscribir.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT cupo_maximo FROM grupos WHERE id = %s", (grupo_id,))
        fila = cursor.fetchone()
        cupo_max = fila[0] if fila else 0

        cursor.execute(
            "SELECT COUNT(*) FROM inscripciones WHERE grupo_id = %s AND estado = 'activo'",
            (grupo_id,)
        )
        inscritos = cursor.fetchone()[0]
        return cupo_max, inscritos
    finally:
        close_connection(conn)


def insertar(idioma_id, nivel_id, docente_id, nombre_grupo, horario, cupo_maximo):
    """
    Inserta un nuevo grupo.
    Verifica que el docente no tenga otro grupo en el mismo horario.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()

        # Regla de negocio: docente sin conflicto de horario
        cursor.execute(
            "SELECT COUNT(*) FROM grupos WHERE docente_id = %s AND horario = %s",
            (docente_id, horario)
        )
        if cursor.fetchone()[0] > 0:
            raise ValueError("El docente ya tiene un grupo en ese horario.")

        cursor.execute(
            "INSERT INTO grupos (idioma_id, nivel_id, docente_id, nombre_grupo, horario, cupo_maximo) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (idioma_id, nivel_id, docente_id, nombre_grupo, horario, cupo_maximo)
        )
        conn.commit()
    finally:
        close_connection(conn)


def actualizar(id_grupo, idioma_id, nivel_id, docente_id, nombre_grupo, horario, cupo_maximo):
    """
    Actualiza los datos de un grupo.
    Verifica conflicto de horario del docente excluyendo el grupo actual.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()

        # Verificar horario del docente excluyendo este mismo grupo
        cursor.execute(
            "SELECT COUNT(*) FROM grupos WHERE docente_id = %s AND horario = %s AND id <> %s",
            (docente_id, horario, id_grupo)
        )
        if cursor.fetchone()[0] > 0:
            raise ValueError("El docente ya tiene un grupo en ese horario.")

        cursor.execute(
            "UPDATE grupos SET idioma_id=%s, nivel_id=%s, docente_id=%s, "
            "nombre_grupo=%s, horario=%s, cupo_maximo=%s WHERE id=%s",
            (idioma_id, nivel_id, docente_id, nombre_grupo, horario, cupo_maximo, id_grupo)
        )
        conn.commit()
    finally:
        close_connection(conn)


def eliminar(id_grupo):
    """
    Elimina un grupo si no tiene inscripciones.
    Lanza ValueError si hay estudiantes inscritos.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM inscripciones WHERE grupo_id = %s",
            (id_grupo,)
        )
        if cursor.fetchone()[0] > 0:
            raise ValueError("No se puede eliminar: el grupo tiene inscripciones activas.")
        cursor.execute("DELETE FROM grupos WHERE id = %s", (id_grupo,))
        conn.commit()
    finally:
        close_connection(conn)
