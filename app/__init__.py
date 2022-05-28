import click
from config import Config
from flask import Flask, current_app
from flask.cli import with_appcontext
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap5()

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    app.cli.add_command(init_db)

    from .main.routes import main_blueprint

    app.register_blueprint(main_blueprint)

    from .auth.routes import auth_blueprint

    app.register_blueprint(auth_blueprint)

    return app


@click.command("init-db")
@with_appcontext
def init_db():
    """Initialize the database based on schema.sql."""
    with current_app.open_resource("schema.sql") as f:
        sql = f.read().decode("UTF-8")
        print(sql)
        db.session.execute(sql)
        db.session.commit()
    click.echo("Initialized the database.")
    # sample data for dev
    account_sql = """
    INSERT INTO accounts (username, password_hash)
    VALUES
        ('asd', 'pbkdf2:sha256:260000$VOOHNytYeLiKZGBV$e24420980f0fd6a2392a4d82f245bc268c59ca1858b9c7189199d7ccd58b8d75');
    """
    db.session.execute(account_sql)

    posts_sql = """
    INSERT INTO posts (author_id, title, body)
    VALUES
        (1, 'Test post please ignore', 'Hello I''m just testing this plz ignore');
    """
    db.session.execute(posts_sql)

    db.session.commit()
