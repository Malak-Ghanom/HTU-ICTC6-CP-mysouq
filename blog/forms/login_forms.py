from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import InputRequired, EqualTo


class LoginForm(FlaskForm):
    email = StringField("Enter your E-mail")
    password = PasswordField("Enter your password")
    submit = SubmitField("Login")
