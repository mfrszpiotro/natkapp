from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    password = PasswordField("pass", validators=[DataRequired()])
    login = SubmitField("Zaloguj")

class SearchForm(FlaskForm):
    search_text = StringField("search")
    search_submit = SubmitField("Szukaj")
    search_reset = SubmitField("Reset")