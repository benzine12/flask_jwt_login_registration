from flask import Flask
import logging
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from extensions import db, bcrypt
from config import Config
from flask import jsonify, request
from models import User
from addon_helper import func_logger

# Configure the root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('app.log')

console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

# Create formatters and add them to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

app = Flask(__name__)

# App Configurations
app.config.from_object(Config)

# Initialize extensions
bcrypt.init_app(app)
db.init_app(app)
jwt = JWTManager(app)

# Open CORS for testing
CORS(app)

# Create database tables
with app.app_context():
    db.create_all()

# Test route
@app.route('/')
@func_logger
def hello_world():
    return {"message": "run"}

@app.route('/register', methods=['POST'])
@func_logger
def register():
    '''Register func
        send username and password for register.'''
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing or invalid JSON in request",
                            "error": "Bad request"}), 400

        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if len(password) >= 10 or len(username) >= 10:
            return jsonify({"msg": "Username or password shoudn't be longer that 10 characters",
                            "error": "Bad request"}), 400
 

        if not username or not password:
            return jsonify({"msg": "Username and password are required",
                            "error": "Bad request"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"msg": "Username already exists",
                            "error": "Something went wrong"}), 409

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "User registered successfully"}), 201

#login func
@app.route('/login', methods=['POST'])
@func_logger
def login():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing or invalid JSON in request",
                            "error": "Bad request"}), 400

        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username or not password:
            return jsonify({"msg": "Username and password are required",
                            "error": "Bad request"}), 400

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return jsonify({"msg": "Welcome back, commander!"}), 200

        return jsonify({"msg": "Invalid username or password",
                        "error": "Something went wrong"}), 401


if __name__ == '__main__':
    app.run(debug=True)