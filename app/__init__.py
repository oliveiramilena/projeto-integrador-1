from flask import Flask
from app import controllers
from app.config import Config
from app.ext import database
import app.models  # noqa: F401


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    database.init_app(app)

    controllers.init_app(app)

    return app
