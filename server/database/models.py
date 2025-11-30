from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date, timezone

from . import db

class Employee(db.Model):
    __tablename__ = "employee"
    
    id_emp: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(nullable=False)
    birthday: Mapped[date] = mapped_column(db.Date, nullable=False)
    id_cit: Mapped[int] = mapped_column(db.ForeignKey("citizenship.id_cit"), nullable=False)
    id_edu: Mapped[int] = mapped_column(db.ForeignKey("education.id_edu"), nullable=False)
    
    citizenship: Mapped["Citizenship"] = db.relationship()
    education: Mapped["Education"] = db.relationship()
    reports: Mapped[list["Report"]] = db.relationship(back_populates="employee")
    
class Report(db.Model):
    __tablename__ = "report"
    
    id_emp: Mapped[int] = mapped_column(db.ForeignKey("employee.id_emp"), primary_key=True)
    num: Mapped[int] = mapped_column(primary_key=True)
    # На postgre можно будет default=func.now()
    date: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))
    id_div: Mapped[int] = mapped_column(db.ForeignKey("division.id_div"), nullable=False)
    id_pos: Mapped[int] = mapped_column(db.ForeignKey("position.id_pos"), nullable=False)
    old_salary: Mapped[float] = mapped_column(db.Numeric(12, 2), nullable=False)
    
    division: Mapped["Division"] = db.relationship()
    position: Mapped["Position"] = db.relationship()
    employee: Mapped["Employee"] = db.relationship(back_populates="reports")
    
class Citizenship(db.Model):
    __tablename__ = "citizenship"
    
    id_cit: Mapped[int] = mapped_column(primary_key=True)
    name_cit: Mapped[str] = mapped_column(nullable=False, unique=True)
    
class Education(db.Model):
    __tablename__ = "education"
    
    id_edu: Mapped[int] = mapped_column(primary_key=True)
    name_edu: Mapped[str] = mapped_column(nullable=False, unique=True)
    
class Division(db.Model):
    __tablename__ = "division"
    
    id_div: Mapped[int] = mapped_column(primary_key=True)
    name_div: Mapped[str] = mapped_column(nullable=False, unique=True)
    
class Position(db.Model):
    __tablename__ = "position"
    
    id_pos: Mapped[int] = mapped_column(primary_key=True)
    name_pos: Mapped[str] = mapped_column(nullable=False, unique=True)
    salary: Mapped[float] = mapped_column(db.Numeric(12, 2), nullable=False)