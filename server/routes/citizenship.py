from logging import getLogger
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from server.config import load_config
from ..database import db
from ..database.models import Citizenship
from ..forms import CitizenshipForm

core = Blueprint("citizenship", __name__, url_prefix="/citizenship")
config = load_config()

logger = getLogger()

@core.route("/")
def show_list():
    items = db.session.execute(db.select(Citizenship)).scalars().all()
    return render_template(
        "layout/list.html",
        page_title="Citizenship",
        header="Гражданства",
        items=items,
        columns={
            "ID": "id_cit",
            "Гражданство": "name_cit",
        },
        pk_attr="id_cit",
        add_endpoint="citizenship.add",
        edit_endpoint="citizenship.edit",
        )

@core.route("/add", methods=["GET", "POST"])
def add():
    form = CitizenshipForm()

    if form.validate_on_submit():
        cit = Citizenship(
            name_cit=form.name_cit.data
        )
        db.session.add(cit)
        
        db.session.commit()
        return redirect(url_for("citizenship.show_list"))
    
    return render_template("layout/add.html", form=form, page_title="Add citizenship", header="Добавить гражданство")

@core.route("/edit/<int:id_cit>", methods=["GET", "POST"])
def edit(id_cit: int):
    cit = db.get_or_404(Citizenship, id_cit)
    form = CitizenshipForm(obj=cit)

    if form.validate_on_submit():
        cit.name_cit = form.name_cit.data
        
        db.session.commit()
        return redirect(url_for("citizenship.show_list"))
    
    return render_template("layout/edit.html", form=form, page_title="Edit citizenship", header="Изменить гражданство")
    