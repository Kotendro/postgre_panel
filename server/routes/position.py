from logging import getLogger
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from server.config import load_config
from ..database import db
from ..database.models import Position
from ..forms import PositionForm

core = Blueprint("position", __name__, url_prefix="/position")
config = load_config()

logger = getLogger()

@core.route("/")
def show_list():
    items = db.session.execute(db.select(Position)).scalars().all()
    return render_template(
        "layout/list.html",
        page_title="Position",
        header="Должности",
        items=items,
        column_names=("ID", "Должность", "Оклад"),
        column_attrs=("id_pos", "name_pos", "salary"),
        pk_attr="id_pos",
        add_endpoint="position.add",
        edit_endpoint="position.edit",
    )

@core.route("/add", methods=["GET", "POST"])
def add():
    form = PositionForm()

    if form.validate_on_submit():
        pos = Position(
            name_pos=form.name_pos.data,
            salary=form.salary.data
        )
        db.session.add(pos)
        
        db.session.commit()
        return redirect(url_for("position.show_list"))
    
    return render_template("layout/add.html", form=form, page_title="Add position", header="Добавить должность")

@core.route("/edit/<int:id_pos>", methods=["GET", "POST"])
def edit(id_pos: int):
    pos = db.get_or_404(Position, id_pos)
    form = PositionForm(obj=pos)

    if form.validate_on_submit():
        pos.name_pos = form.name_pos.data
        pos.salary = form.salary.data
        
        db.session.commit()
        return redirect(url_for("position.show_list"))
    
    return render_template("layout/edit.html", form=form, page_title="Edit position", header="Изменить должность")
    