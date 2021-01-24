from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, SelectField
from wtforms.validators import InputRequired, EqualTo
from wtforms.fields.html5 import EmailField


class EditUserForm(FlaskForm):
    first_name = StringField("Enter your first name")
    last_name = StringField("Enter your last name")
    picture_url = StringField("Enter the URL for a profile picture")
    biography = TextAreaField("Enter your biography")
    submit = SubmitField("Update User")


class AddUserForm(FlaskForm):
    email = EmailField("Enter your Email")
    password = PasswordField('New Password', [InputRequired(), EqualTo(
        'confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("Repeat Password")

    first_name = StringField("Enter your first name")
    last_name = StringField("Enter your last name")
    biography = TextAreaField("Enter your biography")
    role = SelectField('Sign up as', choices=['Admin','Reseller','Buyer'])
    submit = SubmitField("Add User")
