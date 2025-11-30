from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired

class EmployeeAddForm(FlaskForm):
    """Первое добавление соотрудника подразумевает
    назначение на должность (+ подразделение)"""
    fullname = StringField("ФИО", validators=[DataRequired()])
    birthday = DateField("День рождения", validators=[DataRequired()])
    id_cit = SelectField("Гражданство", coerce=int, validators=[DataRequired()])
    id_edu = SelectField("Образование", coerce=int, validators=[DataRequired()])
    id_div = SelectField("Подразделение", coerce=int, validators=[DataRequired()])
    id_pos = SelectField("Должность", coerce=int, validators=[DataRequired()])
    
class EmployeeEditForm(FlaskForm):
    fullname = StringField("ФИО", validators=[DataRequired()])
    birthday = DateField("День рождения", validators=[DataRequired()])
    id_cit = SelectField("Гражданство", coerce=int, validators=[DataRequired()])
    id_edu = SelectField("Образование", coerce=int, validators=[DataRequired()])
