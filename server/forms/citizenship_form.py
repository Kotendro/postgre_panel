from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class CitizenshipForm(FlaskForm):
    name_cit = StringField("Гражданство", validators=[DataRequired()])
