from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta'

class MiFormulario(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    submit = SubmitField('Enviar')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = MiFormulario()
    if form.validate_on_submit():
        nombre = form.nombre.data
        return render_template('resultado.html', nombre=nombre)
    return render_template('formulario.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
