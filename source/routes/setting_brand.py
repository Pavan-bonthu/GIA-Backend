from flask import Blueprint, request, jsonify
from config import conn, cursor

branding_bp = Blueprint('branding', __name__)

@branding_bp.route('/settings/branding', methods=['GET'])
def get_branding_settings():
    location_id = request.args.get('location_id')
    cursor.execute("SELECT TOP 1 * FROM branding_settings WHERE location_id = ?", location_id)
    row = cursor.fetchone()
    if not row:
        return jsonify({'error': 'Branding settings not found'}), 404

    data = {
        'location_id': row.location_id,
        'brand_name': row.brand_name,
        'logo_url': row.logo_url,
        'email_from_name': row.email_from_name,
        'email_from_address': row.email_from_address,
        'email_reply_to': row.email_reply_to
    }
    return jsonify(data)

@branding_bp.route('/settings/branding', methods=['PUT'])
def update_branding_settings():
    data = request.json
    cursor.execute("""
        UPDATE branding_settings SET
            brand_name = ?,
            logo_url = ?,
            email_from_name = ?,
            email_from_address = ?,
            email_reply_to = ?,
            updated_on = GETDATE()
        WHERE location_id = ?
    """, data['brand_name'], data['logo_url'], data['email_from_name'],
         data['email_from_address'], data['email_reply_to'], data['location_id'])
    conn.commit()
    return jsonify({'message': 'Branding settings updated successfully'})