from flask import Blueprint, jsonify
from database import fetch_all

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET'])
def get_settings():
    results = fetch_all("SELECT * FROM Settings")
    return jsonify(results)
