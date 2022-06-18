from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp


class SubmitPostForm(FlaskForm):
    """
    Flask-WTF form for the creation of a new submission.
    Has a regular text field of up to 300 characters, an expandable body field,
    and a selection field that has a list of all subs.
    """

    title = StringField("Title", validators=[DataRequired(), Length(max=300)])
    body = TextAreaField("Body", validators=[DataRequired(), Length(max=5000)])
    sub = SelectField("Subtsohit", validators=[DataRequired()])


class CreateSubForm(FlaskForm):
    """
    Flask-WTF form for the creation of a new submission.
    Has a text field for the name that only allows basic characters,
    and a field for the title that is shown at the top of the page.
    """

    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(min=3, max=30),
            Regexp(
                r"^[A-Za-z0-9_-]+$",
                message="Invalid input. Allowed characters are A-Z a-z 0-9 _ -.",
            ),
        ],
    )
    title = StringField("Title", validators=[DataRequired(), Length(min=3, max=60)])


class CommentForm(FlaskForm):
    """
    Flask-WTF form for a new comment.
    Has only a text field for the comment body that is shown
    below a post.
    """

    body = TextAreaField("Comment", validators=[DataRequired(), Length(max=5000)])
