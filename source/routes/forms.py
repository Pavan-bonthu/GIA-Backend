from flask import Blueprint, request, jsonify
from database import fetch_all

forms_bp = Blueprint('forms', __name__)

@forms_bp.route('/forms', methods=['GET'])
def list_forms():
    status_filter = request.args.get('status')
    patient_id = request.args.get('patient_id')
    practitioner_id = request.args.get('practitioner_id')
    template_id = request.args.get('template_id')

    query = "SELECT * FROM Forms WHERE 1=1"
    params = []

    if status_filter:
        query += " AND status=?"
        params.append(status_filter)
    if patient_id:
        query += " AND patient_id=?"
        params.append(patient_id)
    if practitioner_id:
        query += " AND practitioner_id=?"
        params.append(practitioner_id)
    if template_id:
        query += " AND template_id=?"
        params.append(template_id)

    results = fetch_all(query, params)
    return jsonify(results)

@forms_bp.route('/forms/export/csv', methods=['GET'])
def export_csv():
    # Example: fetch all filtered forms
    results = fetch_all("SELECT * FROM Forms")
    # Implement CSV generation here if needed
    return jsonify({"message": "CSV export placeholder", "data_count": len(results)})

@forms_bp.route('/forms/export/pdf', methods=['GET'])
def export_pdf():
    results = fetch_all("SELECT * FROM Forms")
    # Implement PDF generation here if needed
    return jsonify({"message": "PDF export placeholder", "data_count": len(results)})
