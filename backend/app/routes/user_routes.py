from flask import Blueprint, jsonify, request
from app.models.user_model import Users

# 'user' blueprint instance 
user_bp = Blueprint('user', __name__)

# miscellaneous functions
def generate_user_id():
    current_user_id = Users.retrieve_latest_user_id()
    formatted_user_id = str(current_user_id)
    str_id_num = formatted_user_id[len(formatted_user_id) // 2 :]

    if int(str_id_num) < 1000:
        return (formatted_user_id[:len(formatted_user_id) // 2 ] + f"{int(str_id_num) + 1:03d}")
    else:
        return None

@user_bp.route('/getAllUsers')
def get_users():
    return Users.retrieve_all_users()

@user_bp.route('/getUser/<int:user_id>')
def get_user_by_id(user_id):
    user = Users.retrieve_user_by_id(user_id)
    if user:
        return jsonify({"user": user.to_dict()})
    else:
        return jsonify({"error": "User not found"}), 404
    
@user_bp.route('/getUserByUsername/<string:username>')
def get_user_by_username(username):
    user = Users.retrieve_user_by_username(username)
    if user:
        return jsonify({"user": user.to_dict()})
    else:
        return jsonify({"error": "User not found"}), 404
    
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)
    if data is None:
        data = request.form.to_dict()

    username = data.get('username') if isinstance(data, dict) else None
    password = data.get('password') if isinstance(data, dict) else None

    if not username:
        return jsonify({"error": "username is required"})
    
    if not password:
        return jsonify({"error": "password is required"})

    exists = Users.user_exists(username)

    if not exists:
        return jsonify({"error": "User does not exist"})
    else:
        stored_password = Users.retrieve_password(Users.retrieve_user_id(username))
        if stored_password != password:
            return jsonify({"error": "Invalid password"})
        else:
            return jsonify({"message": "Login successful"})    
        

@user_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json(silent=True)
    if data is None:
        data = request.form.to_dict()

    user_type = data.get('user_type') if isinstance(data, dict) else None
    username = data.get('username') if isinstance(data, dict) else None
    password = data.get('password') if isinstance(data, dict) else None
    full_name = data.get('full_name') if isinstance(data, dict) else None

    if not user_type:
        return jsonify({"error": "user_type is required"})
    if not username:
        return jsonify({"error": "username is required"})
    if not password:
        return jsonify({"error": "password is required"})
    if not full_name:
        return jsonify({"error": "full_name is required"})
    
    exists = Users.user_exists(username)
    if exists:
        return jsonify({"error": "User already exists"})
    else:
        try:
            Users.add_user(
                user_id=generate_user_id(),
                user_role=user_type,
                username=username,
                password=password,
                full_name=full_name
            )

            return jsonify({"message": "User created successfully"})
        
        except Exception as e:
            return jsonify({"error": str(e)})