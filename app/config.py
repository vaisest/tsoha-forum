from os import environ

from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuration class for Flask, which uses dotenv
    to import environment variables from either the .env file
    or regular environment variables.
    Some settings such as the Bootstrap Bootswatch theme are hardcoded.
    See .env.sample for an example.
    """

    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_ENV = environ.get("FLASK_ENV")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI") or environ.get(
        "DATABASE_URL"
    ).replace(
        "postgres://", "postgresql://"
    )  # required because heroku still hasn't updated their URI

    BOOTSTRAP_BOOTSWATCH_THEME = "darkly"
