from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from flask_cors import CORS
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
# open cors for everyone only for testing
CORS(app)

# Configuration
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)

# In-memory blacklist
blacklist = set()

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload['jti'] in blacklist

# Registration route
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return jsonify({"msg": "Create a user by sending a POST request with username and password in JSON format."}), 200
    elif request.method == 'POST':
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
    else:
        return jsonify({"msg": "Method not allowed"}), 405

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.check_password_hash(user.password, password):        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200

# Protected route
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# test func
@app.route('/')
def hello_world():
    return {"message":"run"}

if __name__ == '__main__':
    app.run(debug=True)