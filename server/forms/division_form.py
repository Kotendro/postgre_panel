from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class DivisionForm(FlaskForm):
    name_div = StringField("Подразделение", validators=[DataRequired()])
