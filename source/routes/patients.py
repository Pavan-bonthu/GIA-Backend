from flask import Blueprint, request, jsonify
from config import conn, cursor
from datetime import datetime

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/patients', methods=['GET'])
def get_patients():
    cursor.execute("SELECT id, first_name, last_name, email, phone, dob, created_on FROM patients")
    rows = cursor.fetchall()
    patients = [
        {
            'id': row.id,
            'first_name': row.first_name,
            'last_name': row.last_name,
            'email': row.email,
            'phone': row.phone,
            'dob': row.dob.strftime('%m/%d/%Y') if row.dob else None,
            'created_on': row.created_on.strftime('%m/%d/%Y, %I:%M %p')
        }
        for row in rows
    ]
    return jsonify(patients)

@patients_bp.route('/patients', methods=['POST'])
def create_patient():
    data = request.json
    cursor.execute("""
        INSERT INTO patients (first_name, last_name, email, phone, dob)
        VALUES (?, ?, ?, ?, ?)
    """, data['first_name'], data['last_name'], data.get('email'), data['phone'], data['dob'])
    conn.commit()
    return jsonify({'message': 'Patient created successfully'}), 201

@patients_bp.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    data = request.json
    cursor.execute("""
        UPDATE patients SET first_name = ?, last_name = ?, email = ?, phone = ?, dob = ?
        WHERE id = ?
    """, data['first_name'], data['last_name'], data.get('email'), data['phone'], data['dob'], patient_id)
    conn.commit()
    return jsonify({'message': 'Patient updated successfully'})

@patients_bp.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    cursor.execute("SELECT id, first_name, last_name, email, phone, dob, created_on FROM patients WHERE id = ?", patient_id)
    row = cursor.fetchone()
    if not row:
        return jsonify({'error': 'Patient not found'}), 404
    patient = {
        'id': row.id,
        'first_name': row.first_name,
        'last_name': row.last_name,
        'email': row.email,
        'phone': row.phone,
        'dob': row.dob.strftime('%m/%d/%Y') if row.dob else None,
        'created_on': row.created_on.strftime('%m/%d/%Y, %I:%M %p')
    }
    return jsonify(patient)

@patients_bp.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    cursor.execute("DELETE FROM patients WHERE id = ?", patient_id)
    conn.commit()
    return jsonify({'message': 'Patient deleted successfully'})