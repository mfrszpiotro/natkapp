from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired
from markupsafe import Markup

class LoginForm(FlaskForm):
    password = PasswordField("pass", validators=[DataRequired()])
    login = SubmitField("Zaloguj")

class SearchForm(FlaskForm):
    search_text = StringField("search")