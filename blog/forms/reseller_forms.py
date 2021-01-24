from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, SelectField
from wtforms.validators import InputRequired, EqualTo
from wtforms.fields.html5 import EmailField


class EditItemForm(FlaskForm):

    category = SelectField("Category",choices=[])
    price = StringField("Price")
    title = StringField("Title")
    description = TextAreaField("Description")
    submit = SubmitField("Update Item")


class AddItemForm(FlaskForm):

    category = SelectField("Category",choices=[])
    price = StringField("Price")
    title = StringField("Title")
    description = TextAreaField("Description")
    submit = SubmitField("Add Item")

class RequestCategoryForm(FlaskForm):

    category_name = StringField("Category Name")
    submit = SubmitField("Submit")
