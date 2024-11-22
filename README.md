# Flask JWT Authentication System

A robust Flask application implementing secure user authentication using JSON Web Tokens (JWT). This repository provides a template for implementing user registration, login functionality, and protected routes with token-based authentication.

[![GitHub Repository](https://img.shields.io/badge/GitHub-flask_jwt_login_registration-blue?style=flat&logo=github)](https://github.com/benzine12/flask_jwt_login_registration)

## Project Structure
```
├── app.py              # Main application entry point
├── config.py           # Configuration settings
├── extensions.py       # Flask extensions initialization
├── models.py           # Database models
├── registration.py     # Registration blueprint
├── requirements.txt    # Project dependencies
└── instance/          # Instance-specific files
    └── users.db       # SQLite database
```

## Features

- User registration with secure password hashing using Bcrypt
- Blueprint-based modular architecture
- SQLite database with SQLAlchemy ORM
- CORS support for cross-origin requests
- JWT authentication (configured but not yet implemented)
- Environment-based configuration

## Installation

1. Clone the repository:
```bash
git clone https://github.com/benzine12/flask_jwt_login_registration.git
cd flask_jwt_login_registration
```

2. Create and activate virtual environment:
```bash
# On Windows
python -m venv env
env\Scripts\activate

# On macOS/Linux
python3 -m venv env
source env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## API Endpoints

### 1. Registration
- **URL**: `/auth/register`
- **Method**: `POST`
- **Data**:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```
- **Success Response**: 
  - Code: 201
  - Content: `{"msg": "User registered successfully"}`
- **Error Responses**:
  - Code: 400 - Missing JSON or required fields
  - Code: 409 - Username already exists

### 2. Test Route
- **URL**: `/`
- **Method**: `GET`
- **Success Response**:
```json
{
    "message": "run"
}
```

## Configuration

The application uses the following configuration in `config.py`:

```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'
```

⚠️ **Security Warning**: 
- Change the JWT_SECRET_KEY to a secure value before deployment
- Consider using environment variables for sensitive data
- Enable HTTPS in production
- Configure CORS appropriately for production

## Database Model

```python
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
2. SQLAlchemy for SQL Injection Prevention
3. JWT configuration (ready for implementation)
4. CORS Protection

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