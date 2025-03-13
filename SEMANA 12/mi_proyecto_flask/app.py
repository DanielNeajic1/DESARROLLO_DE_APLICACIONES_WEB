from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import json
import csv

app = Flask(__name__)

# 📌 Ruta de la base de datos
DB_PATH = "database/usuarios.db"

# 📌 Función para conectar a la base de datos SQLite
def conectar_bd():
    return sqlite3.connect(DB_PATH)

# 📌 Función para crear la tabla en SQLite si no existe
def crear_tabla():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

# 📌 Función para guardar datos en TXT
def guardar_en_txt(nombre, correo):
    with open("datos/datos.txt", "a", encoding="utf-8") as f:
        f.write(f"{nombre} - {correo}\n")

# 📌 Función para guardar datos en JSON
def guardar_en_json(nombre, correo):
    archivo = "datos/datos.json"
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        datos = {"usuarios": []}

    datos["usuarios"].append({"nombre": nombre, "correo": correo})

    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4)

# 📌 Función para guardar datos en CSV
def guardar_en_csv(nombre, correo):
    archivo = "datos/datos.csv"
    existe = os.path.isfile(archivo)

    with open(archivo, "a", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        if not existe:
            escritor.writerow(["nombre", "correo"])  # Cabecera si es nuevo
        escritor.writerow([nombre, correo])

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

        # Guardar en SQLite
        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, correo) VALUES (?, ?)", (nombre, correo))
        conexion.commit()
        conexion.close()

        # Guardar en TXT, JSON y CSV
        guardar_en_txt(nombre, correo)
        guardar_en_json(nombre, correo)
        guardar_en_csv(nombre, correo)

        return redirect(url_for('resultado'))
    return render_template('formulario.html')

# 📌 Ruta para ver los datos desde SQLite
@app.route('/resultado')
def resultado():
    conexion = conectar_bd()
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
    crear_tabla()  # Crea la tabla si no existe
    app.run(debug=True)
