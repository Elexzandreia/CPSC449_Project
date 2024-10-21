from flask import Blueprint, request, jsonify
from models import User, db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from sqlalchemy import text
from flask import current_app

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    is_admin = data.get('is_admin', False)

    print(f"Received username: {username}, is_admin: {is_admin}")

    # Ensure unique username
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create a new user
    new_user = User(username=username, password_hash=hashed_password, is_admin=is_admin)

    try:
        db.session.add(new_user)
        db.session.commit()
        print("User created successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error during commit: {e}")
        return jsonify({'error': 'An error occurred during registration'}), 500

    return jsonify({'message': 'User created successfully', 'is_admin': is_admin}), 201


@auth_bp.route('/test-db')
def test_db():
    try:
        with current_app.app_context():  # Ensure the app context is pushed
            result = db.session.execute(text('SELECT 1')).fetchone()
            return f"DB Connection Test Passed! Result: {result[0]}"
    except Exception as e:
        print(f"Error during test-db route execution: {e}")
        return jsonify({'error': 'An error occurred during the DB test', 'details': str(e)}), 500



# Login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user and Bcrypt().check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity={'username': user.username, 'is_admin': user.is_admin})
        return jsonify({'access_token': access_token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401
