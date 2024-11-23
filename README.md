# Flask JWT Authentication System
A robust Flask application implementing secure user authentication using JSON Web Tokens (JWT) with advanced security features including IP blacklisting and brute force protection.

[![GitHub Repository](https://img.shields.io/badge/GitHub-flask_jwt_login_registration-blue?style=flat&logo=github)](https://github.com/benzine12/flask_jwt_login_registration)

## Project Structure
```
├── app.py              # Main application entry point
├── config.py           # Configuration settings
├── extensions.py       # Flask extensions initialization
├── models.py           # Database models
├── registration.py     # Registration blueprint
├── requirements.txt    # Project dependencies
├── addon_helper.py     # Security middleware and decorators
└── instance/          # Instance-specific files
    └── users.db       # SQLite database
```

## Features
- User registration with secure password hashing using Bcrypt
- Blueprint-based modular architecture
- SQLite database with SQLAlchemy ORM
- CORS support for cross-origin requests
- JWT authentication
- Advanced security features:
  - IP blacklisting system
  - Brute force attack protection
  - Username enumeration prevention
  - Request logging and monitoring
  - Suspicious activity detection

## Security Features

### 1. IP Blacklisting
The system maintains a database of suspicious IP addresses and automatically blacklists IPs that:
- Make multiple failed login attempts
- Show signs of username enumeration
- Exhibit suspicious behavior patterns

Blacklisted IPs receive a 403 Forbidden response with a security warning message.

### 2. Brute Force Protection
- Tracks failed login attempts per username
- Automatically blacklists IPs after 3 failed authentication attempts
- Returns masked error messages to prevent information disclosure
- Logs potential brute force attacks for security monitoring

### 3. Username Enumeration Prevention
- Monitors repeated requests for existing usernames
- Implements rate limiting for registration attempts
- Returns consistent error messages regardless of username existence
- Blacklists IPs showing signs of username harvesting (3+ attempts)

### 4. Comprehensive Logging
- Detailed request logging with username tracking
- Error logging with stack traces
- Security incident logging
- IP address monitoring
- Suspicious activity alerts

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
- **URL**: `/register`
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
  - Code: 403 - IP blacklisted

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
  - Code: 200
  - Content: `{"msg": "Welcome back, commander!"}`
- **Error Responses**:
  - Code: 400 - Missing JSON or required fields
  - Code: 401 - Invalid credentials
  - Code: 403 - IP blacklisted

### 3. Test Route
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

## Database Models
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

class IPAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), nullable=False)
    blacklist = db.Column(db.Boolean, default=False)
```

## Security Best Practices
1. Use environment variables for sensitive configuration:
```python
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
```

2. Configure proper CORS settings for production:
```python
CORS(app, resources={r"/api/*": {"origins": "https://yourdomain.com"}})
```

3. Enable HTTPS in production

4. Regular security monitoring:
- Monitor app.log for security incidents
- Review blacklisted IPs periodically
- Analyze failed login patterns
- Monitor for unusual activity spikes

## Development
To run the application in development mode:
```bash
python app.py
```
The server will start at `http://127.0.0.1:5000/`

⚠️ **Security Warnings**: 
- Change the JWT_SECRET_KEY to a secure value before deployment
- Use environment variables for sensitive data
- Enable HTTPS in production
- Configure CORS appropriately for production
- Regularly review security logs and blacklisted IPs
- Consider implementing rate limiting in production
- Monitor for suspicious activity patterns

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