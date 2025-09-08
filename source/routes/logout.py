from flask import Blueprint, jsonify

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout', methods=['POST'])
def logout_user():
    return jsonify({"message": "User logged out successfully"})
