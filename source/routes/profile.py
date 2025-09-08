from flask import Blueprint, jsonify

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
def user_profile():
    profile = {
        "id": 1,
        "name": "John Admin",
        "email": "admin@gia.com",
        "role": "Admin"
    }
    return jsonify(profile)
