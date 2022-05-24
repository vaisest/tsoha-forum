from os import environ

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = environ.get("SECRET_KEY")
    # FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")

    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # debug:
    # SQLALCHEMY_ECHO = True

    BOOTSTRAP_BOOTSWATCH_THEME = "darkly"
