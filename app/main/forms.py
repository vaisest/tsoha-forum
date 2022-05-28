from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class SubmitPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=300)])
    body = TextAreaField("Body", validators=[DataRequired()])
