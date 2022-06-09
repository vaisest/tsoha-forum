from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp


class LoginForm(FlaskForm):
    """
    Flask-WTF form for the login form.
    Has an username which only allows basic characters, and a password field.
    """

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=30),
            Regexp(
                r"^[A-Za-z0-9_-]+$",
                message="Invalid input. Allowed characters are A-Z a-z 0-9 _ -.",
            ),
        ],
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=50)])
    remember_me = BooleanField("Remember Me")


class RegisterForm(FlaskForm):
    """
    Flask-WTF form for the login form.
    Has an username which only allows basic characters, a password field,
    and a password confirmation field that checks for equality.
    """

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=30),
            Regexp(
                r"^[A-Za-z0-9_-]+$",
                message="Invalid input. Allowed characters are A-Z a-z 0-9 _ -.",
            ),
        ],
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=50)])
    password_confirmation = PasswordField(
        "Confirm password", validators=[EqualTo("password", "Passwords do not match.")]
    )
