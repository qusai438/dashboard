from flask import Flask
from .config import Config
from .extensions import mail, cache, socketio
from .tasks import init_celery

celery = init_celery()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    mail.init_app(app)
    cache.init_app(app)
    socketio.init_app(app, message_queue=app.config["CELERY_BROKER_URL"])
    init_celery(app)

    # Register blueprints
    from .blueprints.ads.routes import ads_bp
    from .blueprints.ai_media.routes import ai_media_bp
    from .blueprints.smart_editor.routes import smart_editor_bp
    from .blueprints.returns.routes import returns_bp
    from .blueprints.settings.routes import settings_bp
    from .blueprints.api_keys.routes import api_keys_bp

    app.register_blueprint(ads_bp, url_prefix="/ads")
    app.register_blueprint(ai_media_bp, url_prefix="/ai-media")
    app.register_blueprint(smart_editor_bp, url_prefix="/smart-editor")
    app.register_blueprint(returns_bp, url_prefix="/returns")
    app.register_blueprint(settings_bp, url_prefix="/settings")
    app.register_blueprint(api_keys_bp, url_prefix="/api-keys")

    return app
