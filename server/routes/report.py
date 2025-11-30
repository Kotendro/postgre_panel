from logging import getLogger
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from server.config import load_config
from ..database import db
from ..database.models import Division, Position, Report
from ..forms import ReportForm

core = Blueprint("report", __name__, url_prefix="/report")
config = load_config()

logger = getLogger()

@core.route("/add/<int:id_emp>", methods=["GET", "POST"])
def add(id_emp: int):
    
    form = ReportForm()

    form.id_div.choices = [(d.id_div, d.name_div) for d in Division.query.all()]
    form.id_pos.choices = [(p.id_pos, p.name_pos) for p in Position.query.all()]
    
    last_num: int|None = db.session.execute(
        db.select(db.func.max(Report.num))
        .where(Report.id_emp==id_emp)
    ).scalar_one_or_none()
    next_num = (last_num or 0) + 1

    if form.validate_on_submit():
        old_salary = db.get_or_404(Position, int(form.id_pos.data)).salary
        
        rep = Report(
            id_emp=id_emp,
            num=next_num,
            id_div=form.id_div.data,
            id_pos=form.id_pos.data,
            old_salary=old_salary
        )
        db.session.add(rep)
        db.session.commit()
        return redirect(url_for("employee.detail", id_emp=id_emp))
    
    return render_template("layout/add.html", form=form, page_title="Add report", header="Добавить назначение")

@core.route("/edit/<int:id_emp>/<int:num>", methods=["GET", "POST"])
def edit(id_emp: int, num: int):
    rep = db.get_or_404(Report, (id_emp, num))
    form=ReportForm(obj=rep)

    form.id_div.choices = [(d.id_div, d.name_div) for d in Division.query.all()]
    form.id_pos.choices = [(p.id_pos, p.name_pos) for p in Position.query.all()]

    if form.validate_on_submit():
        rep.id_div=form.id_div.data
        rep.id_pos=form.id_pos.data
        
        db.session.commit()
        return redirect(url_for("employee.detail", id_emp=id_emp))
    
    return render_template("layout/edit.html", form=form, page_title="Edit report", header="Изменить назначение")
    