from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import InputRequired, EqualTo


class LoginForm(FlaskForm):
    email = StringField("Email")
    password = PasswordField("Password")
    submit = SubmitField("Login")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password")
    new_password = PasswordField("New Password",  [InputRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("Confirm Password")
    submit = SubmitField("change")
