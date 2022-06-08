from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class SubmitPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=300)])
    body = TextAreaField("Body", validators=[DataRequired()])
    sub = SelectField("Subtsohit", validators=[DataRequired()])


class CreateSubForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=30)])
    title = StringField("Title", validators=[DataRequired(), Length(min=3, max=60)])
