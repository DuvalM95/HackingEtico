import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    # Insert admin user if not exists
    c.execute('''INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)''', ('admin', 'admin123'))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print('Base de datos inicializada con usuario admin.')
