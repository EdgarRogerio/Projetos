from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
import mysql.connector
import secrets

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = secrets.token_hex(5)

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Edgar123',
    database='meuschema'
)

class Loginform(FlaskForm):
    email = StringField('email', [validators.InputRequired()])
    senha = PasswordField('senha', [validators.InputRequired()])
    senhaconfirma = PasswordField('senhaconfirma', [validators.InputRequired()])
    submit = SubmitField('submit')

@app.route("/", methods=['GET', 'POST'])

def homepage():

    form = Loginform()

    if form.validate_on_submit():

        email = form.email.data
        senha =  form.senha.data
        senhaconfirma = form.senhaconfirma.data

        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Edgar123',
            database='meuschema'
        )

        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO usuarios (email, senha, senhaconfirma) VALUES (%s, %s, %s)', (email, senha, senhaconfirma))
            conn.commit()
            flash('Cadastro realizado com sucesso!', 'success')
        except Exception as e:
            conn.rollback()
            flash('Erro ao cadastrar usuário: ' + str(e), 'error')
        finally:
            cursor.close()
            conn.close()
            
    return render_template("index.html", form=form)

if __name__ == "__main__":
    app.run()