import os


def make_connection_string(host, port, username, password, database):
    return f"postgresql://{username}:{password}@{host}:{port}/{database}"


class Config:
    SQLALCHEMY_DATABASE_URI = make_connection_string(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "54321"),
        username=os.getenv("DB_USERNAME", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        database=os.getenv("DB_NAME", "pi_database"),
    )
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")