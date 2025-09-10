from flask import Blueprint, request, jsonify
from config import conn, cursor

locations_bp = Blueprint('locations', __name__)

@locations_bp.route('/locations', methods=['GET'])
def get_locations():
    cursor.execute("SELECT * FROM locations")
    rows = cursor.fetchall()
    data = [
        {
            'id': row.id,
            'name': row.name,
            'phone': row.phone,
            'timezone': row.timezone,
            'schedule_start': str(row.schedule_start),
            'schedule_end': str(row.schedule_end),
            'address': row.address,
            'apartment_suite': row.apartment_suite,
            'city': row.city,
            'state': row.state,
            'zip_code': row.zip_code,
            'is_active': bool(row.is_active),
            'created_on': row.created_on.strftime('%Y-%m-%d %H:%M:%S')
        }
        for row in rows
    ]
    return jsonify(data)

@locations_bp.route('/locations', methods=['POST'])
def add_location():
    data = request.json
    cursor.execute("""
        INSERT INTO locations (
            name, phone, timezone, schedule_start, schedule_end,
            address, apartment_suite, city, state, zip_code, is_active
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data['name'], data['phone'], data['timezone'], data['schedule_start'], data['schedule_end'],
         data['address'], data.get('apartment_suite', ''), data['city'], data['state'], data['zip_code'], int(data.get('is_active', 1)))
    conn.commit()
    return jsonify({'message': 'Location added successfully'}), 201

@locations_bp.route('/locations/<int:location_id>', methods=['PUT'])
def update_location(location_id):
    data = request.json
    cursor.execute("""
        UPDATE locations SET
            name = ?, phone = ?, timezone = ?, schedule_start = ?, schedule_end = ?,
            address = ?, apartment_suite = ?, city = ?, state = ?, zip_code = ?, is_active = ?
        WHERE id = ?
    """, data['name'], data['phone'], data['timezone'], data['schedule_start'], data['schedule_end'],
         data['address'], data.get('apartment_suite', ''), data['city'], data['state'], data['zip_code'], int(data.get('is_active', 1)), location_id)
    conn.commit()
    return jsonify({'message': 'Location updated successfully'})

@locations_bp.route('/locations/<int:location_id>/toggle', methods=['PATCH'])
def toggle_location_status(location_id):
    cursor.execute("SELECT is_active FROM locations WHERE id = ?", location_id)
    row = cursor.fetchone()
    if not row:
        return jsonify({'error': 'Location not found'}), 404

    new_status = 0 if row.is_active else 1
    cursor.execute("UPDATE locations SET is_active = ? WHERE id = ?", new_status, location_id)
    conn.commit()
    return jsonify({'message': f'Location status updated to {"Active" if new_status else "Inactive"}'})