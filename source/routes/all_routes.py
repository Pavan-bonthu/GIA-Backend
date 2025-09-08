from flask import Blueprint, jsonify

all_routes_bp = Blueprint('all_routes', __name__)

@all_routes_bp.route('/all-routes', methods=['GET'])
def list_routes():
    routes = [
        '/forms', '/patients', '/practitioners', '/templates',
        '/search', '/files', '/analytics', '/nps', '/settings',
        '/profile', '/logout', '/forms/count', '/forms/current', '/staff'
    ]
    return jsonify(routes)
