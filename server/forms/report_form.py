from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired

class ReportForm(FlaskForm):
    id_div = SelectField("Подразделение", coerce=int, validators=[DataRequired()])
    id_pos = SelectField("Должность", coerce=int, validators=[DataRequired()])
    
