from flask import Blueprint, request, jsonify
from database import fetch_all

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
def search_patient():
    q = request.args.get('q', '')
    query = "SELECT * FROM Patients WHERE name LIKE ? OR email LIKE ?"
    param = f"%{q}%"
    results = fetch_all(query, [param, param])
    return jsonify(results)
