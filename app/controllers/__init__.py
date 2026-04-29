from app.controllers.auth import auth
from app.controllers.home import home


def init_app(app):
    app.register_blueprint(home)
    app.register_blueprint(auth)
