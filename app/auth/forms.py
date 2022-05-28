from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=50)])
    remember_me = BooleanField("Remember Me")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=50)])
    password_confirmation = PasswordField(
        "Confirm password", validators=[EqualTo("password", "Passwords do not match.")]
    )
