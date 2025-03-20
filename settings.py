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
SECRET_KEY = os.getenv('SECRET_KEY')  # Do not use a default value in production

# Debug mode should be disabled in production
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

# Configure allowed hosts for production
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Directory for collected static files

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/error.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
