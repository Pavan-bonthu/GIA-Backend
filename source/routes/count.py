from flask import Blueprint, jsonify
from database import fetch_all

count_bp = Blueprint('count_bp', __name__)

@count_bp.route('/forms/count', methods=['GET'])
def forms_count():
    query = "SELECT status, COUNT(*) AS total FROM Forms GROUP BY status"
    results = fetch_all(query)
    return jsonify(results)
