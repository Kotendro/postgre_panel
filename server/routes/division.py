from logging import getLogger
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from server.config import load_config
from ..database import db
from ..database.models import Division
from ..forms import DivisionForm

core = Blueprint("division", __name__, url_prefix="/division")
config = load_config()

logger = getLogger()

@core.route("/")
def show_list():
    items = db.session.execute(db.select(Division)).scalars().all()
    return render_template(
        "layout/list.html",
        page_title="Division",
        header="Подразделения",
        items=items,
        columns={
            "ID": "id_div",
            "Подразделение": "name_div"
        },
        pk_attr="id_div",
        add_endpoint="division.add",
        edit_endpoint="division.edit",
    )

@core.route("/add", methods=["GET", "POST"])
def add():
    form = DivisionForm()

    if form.validate_on_submit():
        div = Division(
            name_div=form.name_div.data
        )
        db.session.add(div)
        
        db.session.commit()
        return redirect(url_for("division.show_list"))
    
    return render_template("layout/add.html", form=form, page_title="Add division", header="Добавить подразделение")

@core.route("/edit/<int:id_div>", methods=["GET", "POST"])
def edit(id_div: int):
    div = db.get_or_404(Division, id_div)
    form = DivisionForm(obj=div)

    if form.validate_on_submit():
        div.name_div = form.name_div.data
        
        db.session.commit()
        return redirect(url_for("division.show_list"))
    
    return render_template("layout/edit.html", form=form, page_title="Edit division", header="Изменить подразделение")
    