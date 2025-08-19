import os
from flask import Flask
from app.core.routes import core_bp

def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(core_bp)
    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)