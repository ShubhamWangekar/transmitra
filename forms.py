from wtforms import TextAreaField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from . import utils

languages_choice = []
for key, value in utils.languages.items() :
    languages_choice.append((key, value))

class Myform(FlaskForm):
    text_field = TextAreaField("Data", validators=[DataRequired()])
    language_field = SelectField("language to translate to", choices=languages_choice )
    submit = SubmitField("Translate")

