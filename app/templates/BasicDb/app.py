from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./database.db"
    app.config["SECRET_KEY"] = "f0b2c9e3d8a14a7e9f6c1b84d5a27e3f4b0c9d18a6e7f52c8d41e9a3b75f0c2e"

    db.init_app(app)
    Migrate(app, db)

    from routes import register_routes
    register_routes(app)

    return app