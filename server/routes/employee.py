from logging import getLogger
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from server.config import load_config
from ..database import db
from ..database.models import Employee, Citizenship, Education, Division, Position, Report
from ..forms import EmployeeAddForm, EmployeeEditForm

core = Blueprint("employee", __name__, url_prefix="/employee")
config = load_config()

logger = getLogger()

@core.route("/")
def show_list():
    employees: list[Employee] = db.session.execute(db.select(Employee)).scalars().all()

    items = []
    for emp in employees:
        last = None
        if emp.reports:
            last = max(emp.reports, key=lambda r: r.num)
            
        items.append({
            "id_emp": emp.id_emp,
            "fullname": emp.fullname,
            "birthday": emp.birthday,
            "name_cit": emp.citizenship.name_cit,
            "name_edu": emp.education.name_edu,
            "name_div": last.division.name_div if last else None,
            "name_pos": last.position.name_pos if last else None,
        })
    
    return render_template(
        "employee/employee_list.html",
        page_title="Employee",
        header="Сотрудники",
        items=items,
        columns={
            "ID": "id_emp",
            "ФИО": "fullname",
            "День рождения": "birthday",
            "Гражданство": "name_cit",
            "Образование": "name_edu",
            "Подразделение": "name_div",
            "Должность": "name_pos",
        },
        pk_attr="id_emp",
        add_endpoint="employee.add",
        detail_endpoint="employee.detail"
    )

@core.route("/add", methods=["GET", "POST"])
def add():
    form = EmployeeAddForm()
    
    form.id_cit.choices = [(c.id_cit, c.name_cit) for c in Citizenship.query.all()]
    form.id_edu.choices = [(e.id_edu, e.name_edu) for e in Education.query.all()]
    form.id_div.choices = [(d.id_div, d.name_div) for d in Division.query.all()]
    form.id_pos.choices = [(p.id_pos, p.name_pos) for p in Position.query.all()]

    if form.validate_on_submit():
        old_salary = db.get_or_404(Position, int(form.id_pos.data)).salary
        
        emp = Employee(
            fullname = form.fullname.data,
            birthday=form.birthday.data,
            id_cit=form.id_cit.data,
            id_edu=form.id_edu.data
        )
        first_report = Report(
            num=1,
            id_div=form.id_div.data,
            id_pos=form.id_pos.data,
            old_salary=old_salary,
            employee=emp
        )
        db.session.add(emp)
        
        db.session.commit()
        return redirect(url_for("employee.show_list"))
    
    return render_template("layout/add.html", form=form, page_title="Add employee", header="Добавить сотрудника")

@core.route("/edit/<int:id_emp>", methods=["GET", "POST"])
def edit(id_emp: int):
    emp = db.get_or_404(Employee, id_emp)
    form = EmployeeEditForm(obj=emp)
    
    form.id_cit.choices = [(c.id_cit, c.name_cit) for c in Citizenship.query.all()]
    form.id_edu.choices = [(e.id_edu, e.name_edu) for e in Education.query.all()]

    if form.validate_on_submit():
        emp.fullname = form.fullname.data
        emp.birthday = form.birthday.data
        emp.id_cit = form.id_cit.data
        emp.id_edu = form.id_edu.data
        
        db.session.commit()
        return redirect(url_for("employee.detail", id_emp=id_emp))
    
    return render_template("layout/edit.html", form=form, page_title="Edit employee", header="Изменить сотрудника")

@core.route("/detail/<int:id_emp>")
def detail(id_emp: int):
    emp: Employee = db.get_or_404(Employee, id_emp)
    
    reports = []
    for report in emp.reports:
        reports.append({
            "num": report.num,
            "date": report.date,
            "name_div": report.division.name_div,
            "name_pos": report.position.name_pos,
            "salary": report.position.salary,
            "old_salary": report.old_salary,
        })
        reports.sort(reverse=True, key=lambda r: r["num"])
    
    employee = {
        "id_emp": emp.id_emp,
        "fullname": emp.fullname,
        "birthday": emp.birthday,
        "name_cit": emp.citizenship.name_cit,
        "name_edu": emp.education.name_edu,
    }
    
    return render_template(
        "employee/employee_detail.html",
        page_title="Employee detail",
        header="Карточка сотрудника",
        employee=employee,
        reports=reports,
        columns_emp={
            "ID": "id_emp",
            "ФИО": "fullname",
            "День рождения": "birthday",
            "Гражданство": "name_cit",
            "Образование": "name_edu",
        },
        columns_rep={
            "№": "num",
            "Дата": "date",
            "Подразделение": "name_div",
            "Должность": "name_pos",
            "Текущий оклад": "salary",
            "Оклад на момент записи": "old_salary"
        },
        edit_emp_endpoint="employee.edit",
        add_rep_endpoint="report.add",
        edit_rep_endpoint="report.edit",
    )
    