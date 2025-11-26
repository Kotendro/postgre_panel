from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from . import db

class Employee(db.Model):
    __tablename__ = "employee"
    
    id_emp: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(nullable=False)
    birthday: Mapped[datetime] = mapped_column(db.DateTime(timezone=True))
    
class Report(db.Model):
    __tablename__ = "report"
    
    id_emp: Mapped
    

    
        
