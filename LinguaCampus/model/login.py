# model/login.py
# Funciones de acceso a datos para la autenticacion de usuarios.

from config.db import get_connection, close_connection


def verificar_usuario(username, password):
    """
    Busca un usuario en la tabla 'usuarios' con las credenciales dadas.
    Retorna el registro si existe, o None si no coincide.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM usuarios WHERE username = %s AND password = %s",
            (username, password)
        )
        return cursor.fetchone()
    finally:
        close_connection(conn)
