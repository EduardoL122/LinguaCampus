# model/idiomas.py
# Funciones de acceso a datos para la tabla 'idiomas'.

from config.db import get_connection, close_connection


def obtener_todos(): # Retorna todos los idiomas ordenados por nombre.
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM idiomas ORDER BY nombre_idioma")
        return cursor.fetchall()
    finally:
        close_connection(conn)


def insertar(nombre): # Inserta un nuevo idioma.
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO idiomas (nombre_idioma) VALUES (%s)",
            (nombre,)
        )
        conn.commit()
    finally:
        close_connection(conn)


def actualizar(id_idioma, nombre): # Actualiaza el nombre de un idioma por su ID.
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE idiomas SET nombre_idioma = %s WHERE id = %s",
            (nombre, id_idioma)
        )
        conn.commit()
    finally:
        close_connection(conn)


def eliminar(id_idioma):
    """
    Elimina un idioma solo si no tiene grupos ni niveles asociados.
    Lanza ValueError si hay registros dependientes.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()

        # Verificar grupos asociados
        cursor.execute(
            "SELECT COUNT(*) FROM grupos WHERE idioma_id = %s",
            (id_idioma,)
        )
        if cursor.fetchone()[0] > 0:
            raise ValueError("No se puede eliminar: el idioma tiene grupos asociados.")

        # Verificar niveles asociados
        cursor.execute(
            "SELECT COUNT(*) FROM niveles WHERE idioma_id = %s",
            (id_idioma,)
        )
        if cursor.fetchone()[0] > 0:
            raise ValueError("No se puede eliminar: el idioma tiene niveles asociados.")

        cursor.execute("DELETE FROM idiomas WHERE id = %s", (id_idioma,))
        conn.commit()
    finally:
        close_connection(conn)
