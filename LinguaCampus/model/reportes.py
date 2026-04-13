# model/reportes.py
# Consultas especiales con JOIN para los reportes del sistema.
# No realiza operaciones CRUD, solo consultas de lectura.

from config.db import get_connection, close_connection


def reporte_aptos_certificacion():
    """
    Retorna los estudiantes con promedio >= 3.5 en algun grupo.
    Se usa para identificar quienes pueden recibir certificado.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT e.nombre          AS estudiante,
                   g.nombre_grupo    AS grupo,
                   i.nombre_idioma   AS idioma,
                   n.nombre          AS nivel,
                   ROUND(AVG(ev.nota), 2) AS promedio
            FROM evaluaciones ev
            JOIN estudiantes e ON ev.estudiante_id = e.id
            JOIN grupos      g ON ev.grupo_id      = g.id
            JOIN idiomas     i ON g.idioma_id      = i.id
            JOIN niveles     n ON g.nivel_id       = n.id
            GROUP BY ev.estudiante_id, ev.grupo_id
            HAVING promedio >= 3.5
            ORDER BY promedio DESC
        """)
        return cursor.fetchall()
    finally:
        close_connection(conn)


def reporte_completo():
    """
    Vista general: estudiante, grupo, idioma, nivel, docente y notas.
    Multiples JOIN para consolidar la informacion.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT e.nombre        AS estudiante,
                   e.email,
                   g.nombre_grupo  AS grupo,
                   g.horario,
                   i.nombre_idioma AS idioma,
                   n.nombre        AS nivel,
                   d.nombre        AS docente,
                   ev.modulo,
                   ev.nota
            FROM inscripciones ins
            JOIN estudiantes e ON ins.estudiante_id = e.id
            JOIN grupos      g ON ins.grupo_id      = g.id
            JOIN idiomas     i ON g.idioma_id       = i.id
            JOIN niveles     n ON g.nivel_id        = n.id
            JOIN docentes    d ON g.docente_id      = d.id
            LEFT JOIN evaluaciones ev
                   ON ev.estudiante_id = ins.estudiante_id
                  AND ev.grupo_id      = ins.grupo_id
            ORDER BY e.nombre, ev.modulo
        """)
        return cursor.fetchall()
    finally:
        close_connection(conn)


def filtrar_estudiantes(idioma_id=None, nivel_id=None, estado_ins=None):
    """
    Filtra estudiantes segun idioma, nivel o estado de inscripcion.
    Los parametros son opcionales; si son None no se aplica ese filtro.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)

        # Consulta base con todos los JOIN necesarios
        query = """
            SELECT DISTINCT e.nombre, e.email, e.estado,
                   i.nombre_idioma   AS idioma,
                   n.nombre          AS nivel,
                   ins.estado        AS estado_inscripcion
            FROM estudiantes e
            JOIN inscripciones ins ON e.id            = ins.estudiante_id
            JOIN grupos        g   ON ins.grupo_id    = g.id
            JOIN idiomas       i   ON g.idioma_id     = i.id
            JOIN niveles       n   ON g.nivel_id      = n.id
            WHERE 1=1
        """
        parametros = []

        # Agregar filtros dinamicamente segun los valores recibidos
        if idioma_id:
            query += " AND g.idioma_id = %s"
            parametros.append(idioma_id)
        if nivel_id:
            query += " AND g.nivel_id = %s"
            parametros.append(nivel_id)
        if estado_ins:
            query += " AND ins.estado = %s"
            parametros.append(estado_ins)

        query += " ORDER BY e.nombre"
        cursor.execute(query, parametros)
        return cursor.fetchall()
    finally:
        close_connection(conn)
