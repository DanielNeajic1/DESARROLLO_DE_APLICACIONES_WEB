import mysql.connector

def conectar_mysql():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1996",  # Agrega tu contraseña si es necesario
            database="desarrollo_web"
        )
        return conexion
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
