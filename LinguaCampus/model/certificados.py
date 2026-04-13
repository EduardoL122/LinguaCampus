# model/certificados.py
# Funciones de acceso a datos para la tabla 'certificados'.

from config.db import get_connection, close_connection


def obtener_todos():
    """
    Retorna todos los certificados con datos del estudiante,
    nivel y grupo usando JOIN.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.id, c.fecha, c.estado,
                   c.estudiante_id, c.nivel_id, c.grupo_id,
                   e.nombre       AS estudiante,
                   n.nombre       AS nivel,
                   g.nombre_grupo AS grupo
            FROM certificados c
            JOIN estudiantes e ON c.estudiante_id = e.id
            JOIN niveles     n ON c.nivel_id      = n.id
            JOIN grupos      g ON c.grupo_id      = g.id
            ORDER BY c.fecha DESC
        """)
        return cursor.fetchall()
    finally:
        close_connection(conn)


def insertar(estudiante_id, nivel_id, grupo_id, fecha, estado):
    """
    Inserta un certificado solo si el promedio del estudiante
    en el grupo es mayor o igual a 3.5.
    Lanza ValueError si no cumple la condicion.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()

        # Regla de negocio: promedio minimo 3.5
        cursor.execute(
            "SELECT nota FROM evaluaciones "
            "WHERE estudiante_id = %s AND grupo_id = %s",
            (estudiante_id, grupo_id)
        )
        fila = cursor.fetchone()
        if fila[0] is None:
            raise ValueError("El estudiante no tiene evaluaciones en este grupo.")
        if float(fila[0]) < 3.5:
            raise ValueError(
                f"Promedio insuficiente ({float(fila[0]):.2f}). Se requiere minimo 3.5."
            )

        cursor.execute(
            "INSERT INTO certificados (estudiante_id, nivel_id, grupo_id, fecha, estado) "
            "VALUES (%s, %s, %s, %s, %s)",
            (estudiante_id, nivel_id, grupo_id, fecha, estado)
        )
        conn.commit()
    finally:
        close_connection(conn)


def actualizar(id_certificado, estudiante_id, nivel_id, grupo_id, fecha, estado): # Actualiza un certificado por su ID
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE certificados SET estudiante_id=%s, nivel_id=%s, grupo_id=%s, "
            "fecha=%s, estado=%s WHERE id=%s",
            (estudiante_id, nivel_id, grupo_id, fecha, estado, id_certificado)
        )
        conn.commit()
    finally:
        close_connection(conn)


def eliminar(id_certificado): # Elimina un certificado por su ID
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM certificados WHERE id = %s", (id_certificado,))
        conn.commit()
    finally:
        close_connection(conn)
