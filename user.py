from flask import Blueprint, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

from models import Resident
from app import db

users = Blueprint('users', __name__)
bcrypt = Bcrypt()  

@users.route('/register', methods=["POST"])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Input validation (ensure email and password exist, etc.)

    user = Resident.query.filter_by(email=email).first()
    if user:
        return jsonify({'error': 'Email already exists'}), 400

    new_user = Resident(email=email, password=password)  # Uses password setter
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@users.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email') 
    password = data.get('password')

    user = Resident.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        access_token = create_access_token(identity=user.resident_id)
        session['user_id'] = user.resident_id 
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@users.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None) 
    return jsonify({'message': 'Logged out successfully'}), 200

@users.route('/whoami')
def whoami():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401  

    user_id = session['user_id']
    return jsonify({'user_id': user_id}), 200