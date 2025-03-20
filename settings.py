import os
from dotenv import load_dotenv  # Import dotenv to load environment variables

load_dotenv()  # Load environment variables from .env file

DATABASES = {
    'default': {
        'ENGINE': 'djongo',  # Ensure you are using the correct MongoDB engine
        'NAME': os.getenv('MONGO_DB_NAME', 'default_db_name'),  # Fallback to 'default_db_name' if not set
        'CLIENT': {
            'host': os.getenv('MONGO_HOST', 'mongodb://localhost:27017/default_db_name'),  # Fallback to localhost
            'authMechanism': os.getenv('DB_AUTH_MECHANISM', 'SCRAM-SHA-1'),  # Default to SCRAM-SHA-1
        }
    }
}

# Ensure SECRET_KEY is loaded from the environment
SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')  # Replace with a secure default for development

# Debug mode should also be configurable via environment variables
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
