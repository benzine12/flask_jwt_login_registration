I'll update the links and make the README more accurate for your specific repository.





# Flask JWT Authentication System

A robust Flask application implementing secure user authentication using JSON Web Tokens (JWT). This repository provides a template for implementing user registration, login functionality, and protected routes with token-based authentication.

[![GitHub Repository](https://img.shields.io/badge/GitHub-flask_jwt_login_registration-blue?style=flat&logo=github)](https://github.com/benzine12/flask_jwt_login_registration)

## Features

- User registration with secure password hashing
- JWT authentication with access and refresh tokens
- Protected routes with JWT verification
- Token blacklisting for secure logout
- SQLite database integration
- CORS support for cross-origin requests

## Installation

1. Clone the repository:
```bash
git clone https://github.com/benzine12/flask_jwt_login_registration.git
cd flask_jwt_login_registration
```

2. Create and activate virtual environment:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Requirements

<antArtifact identifier="requirements" type="application/vnd.ant.code" language="txt" title="requirements.txt">
Flask==3.0.2
Flask-Bcrypt==4.0.1
Flask-Cors==4.0.0
Flask-JWT-Extended==4.6.0
Flask-SQLAlchemy==3.1.1
python-dotenv==1.0.1
Werkzeug==3.0.1
SQLAlchemy==2.0.25
PyJWT==2.8.0


## API Endpoints

### 1. Registration
- **URL**: `/register`
- **Method**: `POST`, `GET`
- **POST Data**:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```
- **Success Response**: 
  - Code: 201
  - Content: `{"msg": "User registered successfully"}`
- **GET Response**:
  - Instructions for creating a user

### 2. Login
- **URL**: `/login`
- **Method**: `POST`
- **Data**:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```
- **Success Response**:
```json
{
    "access_token": "jwt_access_token",
    "refresh_token": "jwt_refresh_token"
}
```

### 3. Protected Route
- **URL**: `/protected`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer your_access_token`
- **Success Response**:
```json
{
    "logged_in_as": "username"
}
```

## Testing with cURL

1. Register a user:
```bash
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}'
```

2. Login:
```bash
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}'
```

3. Access protected route:
```bash
curl -X GET http://127.0.0.1:5000/protected \
  -H "Authorization: Bearer your_access_token"
```

## Configuration

The application uses the following configuration:

```python
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

⚠️ **Security Warning**: 
- Change the JWT_SECRET_KEY to a secure value
- Restrict CORS in production
- Enable HTTPS in production
- Consider using environment variables for sensitive data

## Database

The application uses SQLite with SQLAlchemy. The database is automatically created when you run the application for the first time.

```python
# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
```

## Development

To run the application in development mode:

```bash
python app.py
```

The server will start at `http://127.0.0.1:5000/`

## Security Features

1. Password Hashing using Bcrypt
2. JWT Token Authentication
3. Token Blacklisting
4. CORS Protection
5. SQLAlchemy for SQL Injection Prevention

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Repository

- GitHub: [flask_jwt_login_registration](https://github.com/benzine12/flask_jwt_login_registration)

## License

This project is licensed under the MIT License.
</antArtifact>
