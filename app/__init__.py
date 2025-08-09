from flask import Flask
from flask_cors import CORS
from .extensions import mail, cache, socketio, celery
from .config import Config
import os


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    mail.init_app(app)
    cache.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    celery.conf.update(app.config)

    # Register blueprints dynamically
    from .blueprints import register_blueprints
    register_blueprints(app)

    # Create uploads folder if not exists
    os.makedirs(os.path.join(app.root_path, "static", "uploads"), exist_ok=True)

    return app
