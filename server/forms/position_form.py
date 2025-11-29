from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import DataRequired, NumberRange
from decimal import ROUND_HALF_UP

class PositionForm(FlaskForm):
    name_pos = StringField("Должность", validators=[DataRequired()])
    salary = DecimalField(
        "Оклад",
        places=2,
        rounding=ROUND_HALF_UP,
        render_kw={"step": "0.01"},
        validators=[DataRequired(), NumberRange(min=0,  message="Значение не может быть отрицательным.")]
    )
