from flask import Flask
from flask_migrate import Migrate
from .config import Config
from app.routes import main, socketio
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    socketio.init_app(app, cors_allowed_origins="*", logger=True)

    app.register_blueprint(main)  # Register routes

    return app
