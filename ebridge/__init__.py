# Import the Flask basics
from flask import Flask

# local imports
from config import app_config


def create_app(config_name):
    # Define the App
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    # Import the module / component using their blueprints
    from ebridge.home.views import home
    # Register Blueprints
    app.register_blueprint(home)
    return app
