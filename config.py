import os
from datetime import timedelta

# Project root
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Flask Configuration
class Config:
    # Basic
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Upload
    UPLOAD_FOLDER = os.path.join(BASEDIR, 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}
    
    # Model
    MODEL_PATH = os.path.join(BASEDIR, 'models', 'weights', 're_model.h5')
    IMG_SIZE = 224
    BATCH_SIZE = 1
    
    # Classes
    CLASSES = [
        'Atelectasis',
        'Effusion',
        'Infiltration',
        'No_Finding',
        'Pneumonia'
    ]
    
    # Logging
    LOG_FOLDER = os.path.join(BASEDIR, 'logs')
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False

# Config Dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
