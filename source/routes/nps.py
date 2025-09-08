from flask import Blueprint, jsonify
from database import fetch_all

nps_bp = Blueprint('nps', __name__)

@nps_bp.route('/nps', methods=['GET'])
def nps_feedback():
    results = fetch_all("SELECT patient_name AS patient, score, comment FROM NPS_Feedback")
    return jsonify(results)
