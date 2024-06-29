from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileField, FileRequired


class AddProduct(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    price = IntegerField("Product Price", validators=[DataRequired()])
    image_url = StringField("Product image URL")
    image = FileField("Product image")
    text = StringField("Description")
    category_id = IntegerField("Category Id")

    submit = SubmitField("Submit")


class AddAnimals(FlaskForm):
    animal_name = StringField("Animal Name", validators=[DataRequired()])
    animal_text = StringField("Text About This Animal", validators=[DataRequired()])
    animal_image_url = StringField("Animal image URL")

    submit = SubmitField("Submit")




class Registration(FlaskForm):
    userName = StringField("First Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    phone_Number = StringField("Phone Number", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match")])

    submit = SubmitField("Submit")


class Login(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    submit = SubmitField("Submit")




