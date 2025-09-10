from flask import Blueprint, request, jsonify
from config import conn, cursor
from datetime import datetime

admin_users_bp = Blueprint('admin_users', __name__)

@admin_users_bp.route('/admin/users', methods=['GET'])
def list_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    data = []
    for user in users:
        cursor.execute("""
            SELECT name FROM user_locations ul
            JOIN locations l ON ul.location_id = l.id
            WHERE ul.user_id = ?
        """, user.id)
        locations = [row.name for row in cursor.fetchall()]
        cursor.execute("SELECT name FROM locations WHERE id = ?", user.default_location_id)
        default_location = cursor.fetchone()
        data.append({
            'id': user.id,
            'name': f"{user.first_name} {user.last_name}",
            'email': user.email,
            'mobile_phone': user.mobile_phone,
            'role_group': user.role_group,
            'default_location': default_location.name if default_location else None,
            'locations': locations,
            'last_login': user.last_login.strftime('%Y-%m-%d %I:%M%p') if user.last_login else None,
            'is_active': bool(user.is_active)
        })

    return jsonify(data)

@admin_users_bp.route('/admin/users', methods=['POST'])
def create_user():
    data = request.json
    cursor.execute("""
        INSERT INTO users (first_name, last_name, mobile_phone, email, role_group, default_location_id, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, data['first_name'], data['last_name'], data['mobile_phone'], data['email'],
         data['role_group'], data['default_location_id'], int(data.get('is_active', 1)))
    conn.commit()

    cursor.execute("SELECT SCOPE_IDENTITY()")
    user_id = cursor.fetchone()[0]

    for loc_id in data.get('location_ids', []):
        cursor.execute("INSERT INTO user_locations (user_id, location_id) VALUES (?, ?)", user_id, loc_id)
    conn.commit()

    return jsonify({'message': 'User created successfully', 'user_id': user_id}), 201

@admin_users_bp.route('/admin/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    cursor.execute("""
        UPDATE users SET first_name = ?, last_name = ?, mobile_phone = ?, email = ?,
                         role_group = ?, default_location_id = ?, is_active = ?
        WHERE id = ?
    """, data['first_name'], data['last_name'], data['mobile_phone'], data['email'],
         data['role_group'], data['default_location_id'], int(data.get('is_active', 1)), user_id)
    conn.commit()

    cursor.execute("DELETE FROM user_locations WHERE user_id = ?", user_id)
    for loc_id in data.get('location_ids', []):
        cursor.execute("INSERT INTO user_locations (user_id, location_id) VALUES (?, ?)", user_id, loc_id)
    conn.commit()

    return jsonify({'message': 'User updated successfully'})

@admin_users_bp.route('/admin/users/<int:user_id>/login', methods=['PATCH'])
def update_last_login(user_id):
    now = datetime.utcnow()
    cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", now, user_id)
    conn.commit()
    return jsonify({'message': 'Last login updated'})