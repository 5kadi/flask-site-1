from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, validators
from wtforms.validators import DataRequired, Length

class login_form(FlaskForm):
    username = StringField("Username:", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField("Submit")

class signup_form(FlaskForm):
    username = StringField("Select username:", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Select password:", validators=[DataRequired()])
    submit = SubmitField("Submit")


