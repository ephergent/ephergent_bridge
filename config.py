# config.py
import logging
from logging.config import dictConfig
import os


class Config(object):
    """
    Common configurations
    """
    # Put any configurations here that are common across all environments
    # Name of the app
    APP_NAME = 'app'
    # Threads
    THREADS_PER_PAGE = 2
    # Enable protection against *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True
    # Use a secure, unique and absolutely secret key for
    CSRF_SESSION_KEY = os.getenv('CSRF_SESSION_KEY')
    # Secret key for signing cookies
    SECRET_KEY = os.getenv('SECRET_KEY')
    # Salt for Tokens
    SALTY_SECRET = os.getenv('SALTY_SECRET')
    # Set Logging level
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL')
    # Define logging dict
    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '{"date": "%(asctime)s", '
                          '"log_level": "%(levelname)s", '
                          '"module": "%(module)s", '
                          '"message": "%(message)s"}'
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': 'app.log',
                'maxBytes': 1024000,
                'backupCount': 3
            }
        },
        'root': {
            'level': LOGGING_LEVEL,
            'handlers': [
                'wsgi',
                'file'
            ]
        }
    })


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    FLASK_DEBUG = True
    ENV = 'development'


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    FLASK_DEBUG = False
    ENV = 'production'


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

