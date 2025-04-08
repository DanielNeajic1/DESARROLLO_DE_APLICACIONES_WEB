from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'secret_key'  # Cambia esto por una clave segura en producción

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Cambia esto por tu usuario
app.config['MYSQL_PASSWORD'] = '1996'  # Cambia esto por tu contraseña
app.config['MYSQL_DB'] = 'desarrollo_web'  # Asegúrate de que el nombre sea correcto

mysql = MySQL(app)

# Ruta para la página de inicio
@app.route('/')
def home():
    return redirect(url_for('login'))

# Ruta para el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifica las credenciales (mejora la seguridad en producción)
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('productos'))
        else:
            return 'Credenciales incorrectas, intenta de nuevo.'

    return render_template('login.html')

# Ruta protegida para ver productos
@app.route('/productos')
def productos():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM productos")
        resultados = cursor.fetchall()
        cursor.close()
        return render_template('productos.html', resultados=resultados)
    except Exception as e:
        return f"Error al obtener productos: {str(e)}"

# Ruta para agregar productos
@app.route('/crear_producto', methods=['GET', 'POST'])
def crear_producto():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)", (nombre, precio, stock))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('productos'))
        except Exception as e:
            return f"Error al agregar producto: {str(e)}"

    return render_template('crear_producto.html')

# Ruta para editar productos
@app.route('/editar/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()
    cursor.close()

    if not producto:
        return "Producto no encontrado", 404

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE productos SET nombre=%s, precio=%s, stock=%s WHERE id_producto=%s", (nombre, precio, stock, id_producto))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('productos'))
        except Exception as e:
            return f"Error al actualizar producto: {str(e)}"

    return render_template('editar_producto.html', producto=producto)

# Ruta para eliminar productos
@app.route('/eliminar/<int:id_producto>')
def eliminar_producto(id_producto):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('productos'))
    except Exception as e:
        return f"Error al eliminar producto: {str(e)}"

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
