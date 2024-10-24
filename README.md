Flask JWT Authentication Template

This is a Flask application template that demonstrates how to implement user registration, login, and protected routes using JWT (JSON Web Tokens) for authentication. It utilizes several technologies to create a secure and scalable authentication system.

Technologies Used

	•	Flask: A micro web framework for Python.
	•	Flask-JWT-Extended: Extension for adding JWT support to Flask applications.
	•	Flask-Bcrypt: Extension that provides bcrypt hashing utilities for your application.
	•	Flask-CORS: A Flask extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.
	•	Flask-SQLAlchemy: Adds SQLAlchemy support to your Flask application.
	•	SQLite: A lightweight disk-based database.

Features

	•	User Registration with password hashing.
	•	User Login with JWT token generation.
	•	Token Blacklisting (Logout functionality).
	•	Protected routes accessible only with valid JWT tokens.
	•	CORS support for handling cross-origin requests.

Getting Started

Prerequisites

	•	Python 3.6 or higher installed on your machine.
	•	pip package manager.

Installation

	1.	Clone the Repository

git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name


	2.	Create a Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`


	3.	Install Dependencies

pip install -r requirements.txt

Note: If you don’t have a requirements.txt, you can install the packages individually:

pip install Flask Flask-JWT-Extended Flask-Bcrypt Flask-CORS Flask-SQLAlchemy



Configuration

	•	Open the app.py file.
	•	You can change the JWT_SECRET_KEY to a more secure and unique value.
	•	Adjust other configurations as needed.

Database Setup

	•	The application uses SQLite by default.
	•	The database file (users.db) will be created automatically when you run the application.

Running the Application

python app.py

	•	The application will start in development mode with debug enabled.
	•	Navigate to http://127.0.0.1:5000/ to access the application.

API Endpoints

1. Registration

	•	Endpoint: /register
	•	Method: POST
	•	Description: Register a new user.
	•	Request Body:

{
  "username": "your_username",
  "password": "your_password"
}


	•	Response:
	•	Success (201):

{
  "msg": "User registered successfully"
}


	•	Errors:
	•	Missing JSON data (400)
	•	Username already exists (409)

2. Login

	•	Endpoint: /login
	•	Method: POST
	•	Description: Login an existing user.
	•	Request Body:

{
  "username": "your_username",
  "password": "your_password"
}


	•	Response:
	•	Success (200):

{
  "access_token": "your_access_token",
  "refresh_token": "your_refresh_token"
}


	•	Errors:
	•	Missing credentials (400)
	•	Bad username or password (401)

3. Protected Route

	•	Endpoint: /protected
	•	Method: GET
	•	Description: Access protected content with a valid JWT.
	•	Headers:

Authorization: Bearer your_access_token


	•	Response:
	•	Success (200):

{
  "logged_in_as": "your_username"
}


	•	Errors:
	•	Missing or invalid token (401)

4. Logout (Token Revocation)

	•	Endpoint: /logout
	•	Method: DELETE
	•	Description: Logout the user by revoking the current JWT.
	•	Headers:

Authorization: Bearer your_access_token


	•	Response:
	•	Success (200):

{
  "msg": "Successfully logged out"
}



Testing the API

You can use tools like Postman or cURL to test the API endpoints.

Example using cURL

	1.	Register a User

curl -X POST http://127.0.0.1:5000/register \
-H "Content-Type: application/json" \
-d '{"username":"testuser", "password":"testpass"}'


	2.	Login

curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{"username":"testuser", "password":"testpass"}'

	•	Save the access_token from the response.

	3.	Access Protected Route

curl -X GET http://127.0.0.1:5000/protected \
-H "Authorization: Bearer your_access_token"


	4.	Logout

curl -X DELETE http://127.0.0.1:5000/logout \
-H "Authorization: Bearer your_access_token"


Code Overview

Initialization

	•	Flask Application Setup

app = Flask(__name__)


	•	Extensions Initialization

bcrypt = Bcrypt(app)
CORS(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)


	•	Configuration

app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'



Models

	•	User Model

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)



Authentication Logic

	•	Password Hashing
	•	Registration uses bcrypt.generate_password_hash() to hash passwords.
	•	Login uses bcrypt.check_password_hash() to verify passwords.
	•	JWT Tokens
	•	Access and Refresh tokens are generated using create_access_token() and create_refresh_token().
	•	Protected routes require a valid JWT in the Authorization header.

Token Revocation

	•	Blacklist Mechanism
	•	An in-memory blacklist set stores revoked tokens.
	•	The @jwt.token_in_blocklist_loader decorator checks if a token is revoked.
	•	Logout endpoint adds the token’s JTI to the blacklist.

Error Handling

	•	Custom error messages and status codes are returned for various error scenarios, such as missing data, invalid credentials, and unauthorized access.

Security Considerations

	•	Secret Key
	•	Change the JWT_SECRET_KEY to a secure, unpredictable value.
	•	Consider using environment variables to store secret keys.
	•	HTTPS
	•	For production, ensure the application runs over HTTPS to secure token transmission.
	•	Token Storage
	•	On the client side, store JWT tokens securely, preferably in HTTP-only cookies.
	•	Database Security
	•	If using a production database, ensure secure credentials and connections.

Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss improvements or features.

License

This project is open-source and available under the MIT License.

Acknowledgments

	•	Flask
	•	Flask-JWT-Extended Documentation
	•	Flask-Bcrypt
	•	Flask-CORS
	•	Flask-SQLAlchemy
