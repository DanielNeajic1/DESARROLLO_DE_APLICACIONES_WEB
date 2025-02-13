from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Ruta para la página principal
@app.route("/")
def home():
    return render_template("index.html")

# Ruta para la página "about"
@app.route("/about")
def about():
    return render_template("about.html")

# Ruta para servir el favicon correctamente
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(debug=True)
