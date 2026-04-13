# config/db.py
# Configuracion de la conexion a la base de datos MySQL.
# Cambia user y password segun tu entorno local.

import mysql.connector
from mysql.connector import Error

# Datos de conexion
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "Sena2025*",
    "database": "linguacampus"
}


def get_connection(): # Abre y retorna una conexion activa a la base de datos.
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        raise ConnectionError(f"No se pudo conectar a la base de datos:\n{e}")


def close_connection(conn): # Cierra la conexion si esta abierta.
    if conn and conn.is_connected():
        conn.close()
