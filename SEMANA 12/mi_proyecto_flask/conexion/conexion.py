# Conexión/conexion.py
import mysql.connector
from mysql.connector import Error

def conectar_mysql():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            database='aplicaciones_app',
            user='root',
            password='1996'  # Cambia 'tu_contraseña' por la contraseña de tu base de datos
        )
        if conexion.is_connected():
            print("Conexión exitosa a MySQL")
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None
