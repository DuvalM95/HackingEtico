from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'clave-secreta'

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'tu_contraseña',
    'database': 'login_db'
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        db = get_db()
        cursor = db.cursor()
        if usuario == 'admin':
            cursor.execute('SELECT * FROM usuarios WHERE usuario=%s AND contrasena=%s', (usuario, contrasena))
            admin = cursor.fetchone()
            if admin:
                session['admin'] = True
                return redirect(url_for('admin'))
            else:
                return render_template('login.html', error='Admin no válido')
        else:
            cursor.execute('INSERT INTO usuarios (usuario, contrasena) VALUES (%s, %s)', (usuario, contrasena))
            db.commit()
            return render_template('login.html', mensaje='Datos enviados')
    return render_template('login.html')

@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT usuario, contrasena FROM usuarios WHERE usuario != "admin"')
    datos = cursor.fetchall()
    return render_template('admin.html', datos=datos)

if __name__ == '__main__':
    app.run(debug=True)
