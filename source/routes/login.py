from flask import Blueprint, request, jsonify
import jwt, datetime
from config import SECRET_KEY, conn, cursor

login = Blueprint('login', __name__)

@login.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    admin_code = data.get('admin_code', '')

    if not username or not password:
        return jsonify({'status': 'fail', 'message': 'Username and password required'}), 400

    # Fetch user
    cursor.execute("SELECT password FROM users WHERE username = ?", username)
    row = cursor.fetchone()

    if not row:
        return jsonify({'status': 'fail', 'message': 'User not found'}), 404

    stored_password = row[0]
    if stored_password != password:
        return jsonify({'status': 'fail', 'message': 'Incorrect password'}), 401

    # Assign role dynamically
    role = 'Admin' if admin_code == 'Admin123' or username.lower() == 'admin@example.com' else 'Customer'

    # Generate token
    expiry = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({'username': username, 'role': role, 'exp': expiry}, SECRET_KEY, algorithm='HS256')
    redirect_url = '/admin/dashboard' if role == 'Admin' else '/customer/home'

    return jsonify({
        'message': 'Login successful',
        'username': username,
        'role': role,
        'access_token': token,
        'expiry': expiry.isoformat() + 'Z',
        'redirect_url': redirect_url
    })