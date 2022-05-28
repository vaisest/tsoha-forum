from os import environ

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = environ.get("SECRET_KEY")
    # FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI") or environ.get(
        "DATABASE_URL"
    ).replace("postgres://", "postgresql://")

    BOOTSTRAP_BOOTSWATCH_THEME = "darkly"