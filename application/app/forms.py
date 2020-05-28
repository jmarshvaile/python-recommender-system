import json
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired

from app import app

class SelectForm(FlaskForm):
    filepath = 'static/select_form_values.json'
    with app.open_resource(filepath) as file:
        choices = json.load(file)
    select = SelectField('Games', choices=[('', '')] + choices, validators=[InputRequired()])
    submit = SubmitField('Find Similar')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')