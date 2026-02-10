# admin endpoint example
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = data.get('user')
    password = data.get('password')
    if user == 'admin':
        return jsonify({'status': 'success', 'user': user, 'password': password})
    return jsonify({'status': 'fail'}), 401

@app.route('/admin', methods=['GET'])
def admin():
    return jsonify({'message': 'Bienvenido, admin'}), 200

if __name__ == '__main__':
    app.run(debug=True)
