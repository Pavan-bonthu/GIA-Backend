from flask import Blueprint, jsonify
from database import fetch_all

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/staff', methods=['GET'])
def get_staff():
    query = "SELECT * FROM Staff"
    results = fetch_all(query)
    return jsonify(results)
