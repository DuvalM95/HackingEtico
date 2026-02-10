from flask import Flask, request, jsonify, render_template
import sqlite3

import os
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
    static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
)

@app.route('/')
def home():
    return render_template('index.html')

def check_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# Guardar intentos de login
def log_attempt(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('INSERT INTO attempts (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = data.get('user')
    password = data.get('password')
    log_attempt(user, password)
    if check_user(user, password):
        return jsonify({'status': 'success', 'user': user, 'password': password})
    return jsonify({'status': 'fail'}), 401

@app.route('/admin/attempts', methods=['GET'])
def view_attempts():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username, password, timestamp FROM attempts ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return jsonify({'attempts': rows})

if __name__ == '__main__':
    app.run(debug=True)
