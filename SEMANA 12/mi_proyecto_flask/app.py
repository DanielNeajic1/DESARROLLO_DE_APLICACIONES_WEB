# app.py

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Crear la base de datos si no existe
db_path = 'database/usuarios.db'
os.makedirs(os.path.dirname(db_path), exist_ok=True)


def conectar_bd():
    conexion = sqlite3.connect(db_path)
    return conexion


# Crear tabla si no existe
def inicializar_bd():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()


inicializar_bd()


# Ruta de inicio
@app.route('/')
def index():
    return render_template('index.html')


# Ruta para mostrar formulario
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']

        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, correo) VALUES (?, ?)", (nombre, correo))
        conexion.commit()
        conexion.close()

        return redirect(url_for('resultado'))
    return render_template('formulario.html')


# Ruta para mostrar los resultados
@app.route('/resultado')
def resultado():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conexion.close()
    return render_template('resultado.html', usuarios=usuarios)


if __name__ == '__main__':
    app.run(debug=True)