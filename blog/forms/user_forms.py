from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, SelectField, DateField
from wtforms.validators import InputRequired, EqualTo
from wtforms.fields.html5 import EmailField


class EditUserForm(FlaskForm):
    first_name = StringField("Enter your first name")
    last_name = StringField("Enter your last name")
    birthdate = DateField("Enter your birthdate")
    submit = SubmitField("Update User")


class AddUserForm(FlaskForm):
    email = EmailField("Enter your Email")
    password = PasswordField('New Password', [InputRequired(), EqualTo(
        'confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("Repeat Password")

    first_name = StringField("Enter your first name")
    last_name = StringField("Enter your last name")
    birthdate = DateField("Enter your birthdate")
    role = SelectField('Sign up as', choices=['Admin','Reseller','Buyer'])
    submit = SubmitField("Add User")
