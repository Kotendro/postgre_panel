from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class EducationForm(FlaskForm):
    name_edu = StringField("Образование", validators=[DataRequired()])
