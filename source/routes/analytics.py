from flask import Blueprint, jsonify
from database import fetch_all

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics', methods=['GET'])
def analytics_data():
    total_forms = fetch_all("SELECT COUNT(*) AS total FROM Forms")[0]['total']
    total_patients = fetch_all("SELECT COUNT(*) AS total FROM Patients")[0]['total']
    total_practitioners = fetch_all("SELECT COUNT(*) AS total FROM Practitioners")[0]['total']
    
    data = {
        "forms_submitted": total_forms,
        "patients_registered": total_patients,
        "active_practitioners": total_practitioners
    }
    return jsonify(data)
