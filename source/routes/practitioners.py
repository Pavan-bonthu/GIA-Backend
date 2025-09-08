from flask import Blueprint, jsonify
from database import fetch_all

practitioners_bp = Blueprint('practitioners', __name__)

@practitioners_bp.route('/practitioners', methods=['GET'])
def all_practitioners():
    results = fetch_all("SELECT * FROM Practitioners")
    return jsonify(results)
