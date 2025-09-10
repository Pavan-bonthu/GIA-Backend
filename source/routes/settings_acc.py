from flask import Blueprint, request, jsonify
from config import conn, cursor

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings/account', methods=['GET'])
def get_account_settings():
    cursor.execute("SELECT TOP 1 * FROM settings")
    row = cursor.fetchone()
    if not row:
        return jsonify({'error': 'Settings not found'}), 404

    data = {
        'organization_name': row.organization_name,
        'min_age_required': row.min_age_required,
        'verify_dob_access': bool(row.verify_dob_access),
        'label_patients': row.label_patients,
        'label_appointments': row.label_appointments,
        'label_practitioners': row.label_practitioners,
        'label_clinical_notes': row.label_clinical_notes,
        'show_signature_timestamps': bool(row.show_signature_timestamps)
    }
    return jsonify(data)

@settings_bp.route('/settings/account', methods=['PUT'])
def update_account_settings():
    data = request.json
    cursor.execute("""
        UPDATE settings SET
            organization_name = ?,
            min_age_required = ?,
            verify_dob_access = ?,
            label_patients = ?,
            label_appointments = ?,
            label_practitioners = ?,
            label_clinical_notes = ?,
            show_signature_timestamps = ?
        WHERE id = 1
    """, data['organization_name'], data['min_age_required'], int(data['verify_dob_access']),
         data['label_patients'], data['label_appointments'], data['label_practitioners'],
         data['label_clinical_notes'], int(data['show_signature_timestamps']))
    conn.commit()
    return jsonify({'message': 'Settings updated successfully'})
