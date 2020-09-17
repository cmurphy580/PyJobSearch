from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
"""
Login form will ensure the different input fields
are filled and assigned them to particular variable.
"""


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me!")
    submit = SubmitField("Login")


class FilterDataForm(FlaskForm):
    searched = StringField("")
    submit = SubmitField("Search")


class FavoritesForm(FlaskForm):
    add_to_favorites = BooleanField()
