from flask import Blueprint, request, jsonify
import jwt
from config import SECRET_KEY

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return jsonify({'status': 'fail', 'message': 'Token missing'}), 400

    # Optionally decode and blacklist
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        # Add token to blacklist (e.g., Redis or DB)
        # blacklist.add(token)
        return jsonify({'message': 'Logout successful'})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token already expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401