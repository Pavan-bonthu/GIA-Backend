from flask import Blueprint, jsonify
from database import fetch_all

templates_bp = Blueprint('templates', __name__)

@templates_bp.route('/templates', methods=['GET'])
def list_templates():
    results = fetch_all("SELECT * FROM Templates")
    return jsonify(results)
