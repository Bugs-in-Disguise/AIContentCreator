from flask import Flask
from flask_migrate import Migrate
from .config import Config
from app.routes import main, login_manager
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    
    login_manager.init_app(app)

    app.register_blueprint(main)  # Register routes

    return app
