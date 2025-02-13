from flask import Flask, render_template, request, redirect, url_for
import json
import csv
from Conexion.conexion import conectar_mysql  # Importa la función de conexión a MySQL

app = Flask(__name__)

# 📌 Función para crear la tabla en MySQL si no existe
def crear_tabla_mysql():
    conexion = conectar_mysql()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                correo VARCHAR(255) NOT NULL
            )
        """)
        conexion.commit()
        conexion.close()

# 📌 Función para guardar datos en MySQL
def guardar_en_mysql(nombre, correo):
    conexion = conectar_mysql()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, correo) VALUES (%s, %s)", (nombre, correo))
        conexion.commit()
        conexion.close()

# 📌 Ruta para verificar la conexión a MySQL
@app.route('/test_db')
def test_db():
    conexion = conectar_mysql()
    if conexion:
        return "Conexión exitosa a la base de datos MySQL!"
    else:
        return "Error en la conexión a MySQL."

# 📌 Ruta principal (Inicio)
@app.route('/')
def index():
    return render_template('index.html')

# 📌 Ruta del formulario
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']

        # Guardar en MySQL
        guardar_en_mysql(nombre, correo)

        # Guardar en TXT, JSON y CSV
        guardar_en_txt(nombre, correo)
        guardar_en_json(nombre, correo)
        guardar_en_csv(nombre, correo)

        return redirect(url_for('resultado'))
    return render_template('formulario.html')

# 📌 Ruta para ver los datos desde MySQL
@app.route('/resultado')
def resultado():
    conexion = conectar_mysql()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, correo FROM usuarios")
        usuarios = cursor.fetchall()
        conexion.close()
        return render_template('resultado.html', usuarios=usuarios)

# 📌 Ruta para ver los datos desde TXT
@app.route('/ver_txt')
def ver_txt():
    with open("datos/datos.txt", "r", encoding="utf-8") as f:
        contenido = f.readlines()
    return render_template("resultado.html", usuarios=[line.strip().split(" - ") for line in contenido])

# 📌 Ruta para ver los datos desde JSON
@app.route('/ver_json')
def ver_json():
    with open("datos/datos.json", "r", encoding="utf-8") as f:
        datos = json.load(f)
    return render_template("resultado.html", usuarios=[[u["nombre"], u["correo"]] for u in datos["usuarios"]])

# 📌 Ruta para ver los datos desde CSV
@app.route('/ver_csv')
def ver_csv():
    with open("datos/datos.csv", "r", encoding="utf-8") as f:
        lector = csv.reader(f)
        next(lector)  # Saltamos la cabecera
        datos = [fila for fila in lector]
    return render_template("resultado.html", usuarios=datos)

# 📌 Ejecutar la aplicación
if __name__ == '__main__':
    crear_tabla_mysql()  # Crea la tabla si no existe
    app.run(debug=True)
