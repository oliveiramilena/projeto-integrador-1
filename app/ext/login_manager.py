from flask_login import LoginManager

login_manager = LoginManager()


def init_app(app):
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
