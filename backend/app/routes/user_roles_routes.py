from flask import Blueprint, jsonify
from app.models.user_roles_model import UserRoles

user_roles_bp = Blueprint('user_roles', __name__)

@user_roles_bp.route('/getAllRoles')
def get_all_roles():
    roles = UserRoles.retrieve_all_roles()
    return jsonify({"roles": roles})