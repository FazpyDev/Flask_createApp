from flask import Flask, Blueprint


def create_app():
    app = Flask(__name__)

    from Blueprints.core.routes import core
    app.register_blueprint(core, url_prefix="/")

    return app
