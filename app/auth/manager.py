from flask_login import UserMixin
from sqlalchemy.sql import text

from .. import db_service, login_manager


class User(UserMixin):
    """
    Very basic user class for Flask-Login.
    The required static method get and utility method get_by_username
    are implemented by the db_service.
    """

    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def get(user_id):
        return db_service.get_user_by_id(user_id)

    @staticmethod
    def get_by_username(username):
        return db_service.get_user_by_username(username)

    def __str__(self):
        return f"User(Id={self.id}, username={self.username})"


@login_manager.user_loader
def load_user(user_id):
    """Callback for Flask-Login user loading."""
    return User.get(user_id)
