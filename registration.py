from flask import Blueprint, jsonify, request
from extensions import bcrypt, db
from models import User

registration = Blueprint('registration', __name__)

@registration.route('/register', methods=['POST'])
def register():
    '''Register func
        send username and password for register.'''
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing or invalid JSON in request"}), 400

        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username or not password:
            return jsonify({"msg": "Username and password are required"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"msg": "Username already exists"}), 409

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "User registered successfully"}), 201