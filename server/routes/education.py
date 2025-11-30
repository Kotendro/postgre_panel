from logging import getLogger
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from server.config import load_config
from ..database import db
from ..database.models import Education
from ..forms import EducationForm

core = Blueprint("education", __name__, url_prefix="/education")
config = load_config()

logger = getLogger()

@core.route("/")
def show_list():
    items = db.session.execute(db.select(Education)).scalars().all()
    return render_template(
        "layout/list.html",
        page_title="Education",
        header="Образования",
        items=items,
        columns={
            "ID": "id_edu",
            "Образование": "name_edu"
        },
        pk_attr="id_edu",
        add_endpoint="education.add",
        edit_endpoint="education.edit",
    )

@core.route("/add", methods=["GET", "POST"])
def add():
    form = EducationForm()

    if form.validate_on_submit():
        edu = Education(
            name_edu=form.name_edu.data
        )
        db.session.add(edu)
        
        db.session.commit()
        return redirect(url_for("education.show_list"))
    
    return render_template("layout/add.html", form=form, page_title="Add education", header="Добавить образоване")

@core.route("/edit/<int:id_edu>", methods=["GET", "POST"])
def edit(id_edu: int):
    edu = db.get_or_404(Education, id_edu)
    form = EducationForm(obj=edu)

    if form.validate_on_submit():
        edu.name_edu = form.name_edu.data
        
        db.session.commit()
        return redirect(url_for("education.show_list"))
    
    return render_template("layout/edit.html", form=form, page_title="Edit education", header="Изменить образоване")
    