from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired

class EmployeeForm(FlaskForm):
    fullname = StringField("ФИО", validators=[DataRequired()])
    birthday = DateField("День рождения", validators=[DataRequired()])
    id_cit = SelectField("Гражданство", coerce=int, validators=[DataRequired()])
    id_edu = SelectField("Образование", coerce=int, validators=[DataRequired()])
