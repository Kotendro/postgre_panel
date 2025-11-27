from logging import getLogger
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from server.config import load_config
from ..database import db
from ..database.models import Employee, Citizenship, Education
from ..forms import EmployeeForm

core = Blueprint("employee", __name__, url_prefix="/employee")
config = load_config()

logger = getLogger()

@core.route("/")
def show_list():
    emps = db.session.execute(db.select(Employee)).scalars().all()
    return render_template("employee/employee_list.html", emps=emps)

@core.route("/add", methods=["GET", "POST"])
def add():
    form = EmployeeForm()
    
    form.id_cit.choices = [(c.id_cit, c.name_cit) for c in Citizenship.query.all()]
    form.id_edu.choices = [(e.id_edu, e.name_edu) for e in Education.query.all()]

    if form.validate_on_submit():
        emp = Employee(
            fullname = form.fullname.data,
            birthday=form.birthday.data,
            id_cit=form.id_cit.data,
            id_edu=form.id_edu.data
        )
        db.session.add(emp)
        
        db.session.commit()
        return redirect(url_for("employee.show_list"))
    
    return render_template("employee/employee_form.html", form=form)

@core.route("/edit/<int:id_emp>", methods=["GET", "POST"])
def edit_form(id_emp: int):
    emp = db.get_or_404(Employee, id_emp)
    form = EmployeeForm(obj=emp)
    
    form.id_cit.choices = [(c.id_cit, c.name_cit) for c in Citizenship.query.all()]
    form.id_edu.choices = [(e.id_edu, e.name_edu) for e in Education.query.all()]

    if form.validate_on_submit():
        emp.fullname = form.fullname.data
        emp.birthday = form.birthday.data
        emp.id_cit = form.id_cit.data
        emp.id_edu = form.id_edu.data
        
        db.session.commit()
        return redirect(url_for("employee.show_list"))
    
    return render_template("employee/employee_form.html", form=form)
    