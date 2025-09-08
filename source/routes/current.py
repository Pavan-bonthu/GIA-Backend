from flask import Blueprint, jsonify
from database import fetch_all

current_bp = Blueprint('current_bp', __name__)

@current_bp.route('/forms/current', methods=['GET'])
def current_forms():
    query = "SELECT * FROM Forms WHERE status='current'"
    results = fetch_all(query)
    return jsonify(results)
