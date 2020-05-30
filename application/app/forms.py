from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import InputRequired

from app import app

class GameSelectForm(FlaskForm): 
    game_select = SelectField(validators=[InputRequired()])
    game_submit = SubmitField('Submit')
    
class TagSelectForm(FlaskForm): 
    tag_select = SelectField(validators=[InputRequired()])
    tag_submit = SubmitField('Submit')