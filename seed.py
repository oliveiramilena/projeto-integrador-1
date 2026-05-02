from werkzeug.security import generate_password_hash
from app import create_app
from app.ext.database import db
from app.models.user import User


def seed():
    app = create_app()
    with app.app_context():
        if User.query.filter_by(email="test@example.com").first():
            print("Usuário de testes já existe, pulando.")
            return

        user = User(
            name="Usuário de Testes",  # type: ignore
            email="test@example.com",  # type: ignore
            password=generate_password_hash("password123"),  # type: ignore
        )
        db.session.add(user)
        db.session.commit()
        print(f"Usuário criado: {user.email}")


if __name__ == "__main__":
    seed()
