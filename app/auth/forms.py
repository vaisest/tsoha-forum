from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp


class LoginForm(FlaskForm):
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
