from sqlalchemy.dialects import postgresql
from ..models import Division, Report, Employee
from .. import db
from logging import getLogger

logger = getLogger(__name__)

def get_division_show_list():
    
    last_report_subq = (
    db.select(
        Report.id_emp,
        db.func.max(Report.num).label("num")
    )
    .group_by(Report.id_emp)
    .subquery()
    )
    
    stmt = (
        db.select(
            Division,
            db.func.count(last_report_subq.c.id_emp).label("emp_count")
        )
        .outerjoin(
            Report,
            Report.id_div == Division.id_div
        )
        .outerjoin(
            last_report_subq,
            db.and_(
                last_report_subq.c.id_emp == Report.id_emp,
                last_report_subq.c.num == Report.num,
            )
        )
        .outerjoin(
            Employee,
            Employee.id_emp == Report.id_emp
        )
        .group_by(Division.id_div)
        .order_by(Division.id_div)
    )
    rows = db.session.execute(stmt).all()
    
    sql = stmt.compile(
    dialect=postgresql.dialect(),
    compile_kwargs={"literal_binds": True}
    )
    logger.info(sql)
    
    items = []
    for division, count in rows:
        items.append({
            "id_div": division.id_div,
            "name_div": division.name_div,
            "emp_count": count,
        })
    return items