from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from extensions import db, bcrypt
from registration import registration
from config import Config

app = Flask(__name__)

# App Configurations
app.config.from_object(Config)

# Initialize extensions
bcrypt.init_app(app)
db.init_app(app)
jwt = JWTManager(app)

# Open CORS for testing
CORS(app)

# Register Blueprints
app.register_blueprint(registration, url_prefix='/auth')

# Create database tables
with app.app_context():
    db.create_all()

# Test route
@app.route('/')
def hello_world():
    return {"message": "run"}

if __name__ == '__main__':
    app.run(debug=True)