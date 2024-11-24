from datetime import timedelta


class Config:
    # Your existing config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = '' # add your secret key
    JWT_ALGORITHM = "HS256"
    JWT_DECODE_ALGORITHMS = ["HS256"]
    JWT_TOKEN_LOCATION = ["headers"]
    
    # Additional security settings
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  
    JWT_HEADER_TYPE = "Bearer" 
    JWT_HEADER_NAME = "Authorization" 