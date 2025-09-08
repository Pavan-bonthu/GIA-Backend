from flask import Blueprint, jsonify
from database import fetch_all

files_bp = Blueprint('files', __name__)

@files_bp.route('/files', methods=['GET'])
def list_files():
    results = fetch_all("SELECT * FROM Files")
    return jsonify(results)
