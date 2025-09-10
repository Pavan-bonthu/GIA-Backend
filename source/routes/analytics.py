from flask import Blueprint, request, jsonify
from config import conn, cursor

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics/forms', methods=['GET'])
def get_form_analytics():
    view = request.args.get('view', 'summary')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({'error': 'Missing date range'}), 400

    if view == 'detail':
        cursor.execute("""
            SELECT p.first_name + ' ' + p.last_name AS name,
                   fs.status, fs.due_date, fs.email_sent, fs.sms_sent,
                   fs.created, fs.location
            FROM form_status fs
            JOIN patients p ON fs.patient_id = p.id
            WHERE fs.created BETWEEN ? AND ?
        """, start_date, end_date)
        rows = cursor.fetchall()
        data = [
            {
                'name': row.name,
                'status': row.status,
                'due_date': row.due_date,
                'email_sent': row.email_sent,
                'sms_sent': row.sms_sent,
                'created': row.created,
                'location': row.location
            }
            for row in rows
        ]

    elif view == 'intake_method':
        cursor.execute("""
            SELECT intake_method, COUNT(*) AS patient_count
            FROM patients
            WHERE created_on BETWEEN ? AND ?
            GROUP BY intake_method
        """, start_date, end_date)
        rows = cursor.fetchall()
        data = [
            {
                'intake_method': row.intake_method,
                'patient_count': row.patient_count
            }
            for row in rows
        ]

    else:  # summary view
        cursor.execute("""
            SELECT location,
                   COUNT(*) AS total_forms,
                   SUM(CASE WHEN status = 'Assigned' THEN 1 ELSE 0 END) AS assigned,
                   SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed
            FROM form_status
            WHERE created BETWEEN ? AND ?
            GROUP BY location
        """, start_date, end_date)
        rows = cursor.fetchall()
        data = [
            {
                'location': row.location,
                'total_forms': row.total_forms,
                'assigned': row.assigned,
                'completed': row.completed,
                'completion_rate': f"{(row.completed / row.total_forms * 100):.0f}%" if row.total_forms else "0%"
            }
            for row in rows
        ]

    return jsonify({'view': view, 'start_date': start_date, 'end_date': end_date, 'data': data})