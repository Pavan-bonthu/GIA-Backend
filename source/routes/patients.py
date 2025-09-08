from flask import Blueprint, request, jsonify
from database import fetch_all

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/patients', methods=['GET'])
def get_patients():
    query_param = request.args.get('q', '')
    query = "SELECT * FROM Patients WHERE name LIKE ? OR email LIKE ?"
    param = f"%{query_param}%"
    results = fetch_all(query, [param, param])
    return jsonify(results)
