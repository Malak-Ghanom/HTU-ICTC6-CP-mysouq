from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, SelectField
from wtforms.validators import InputRequired, EqualTo
from wtforms.fields.html5 import EmailField


class AddCategoryForm(FlaskForm):

    category_name = StringField("Category Name")
    submit = SubmitField("Submit")
