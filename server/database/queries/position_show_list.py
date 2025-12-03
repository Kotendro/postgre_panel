from sqlalchemy.dialects import postgresql
from ..models import Position, Report, Employee
from .. import db
from logging import getLogger

logger = getLogger(__name__)

def get_position_show_list():
    
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
            Position,
            db.func.count(last_report_subq.c.id_emp).label("emp_count")
        )
        .outerjoin(
            Report,
            Report.id_pos == Position.id_pos
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
        .group_by(Position.id_pos)
        .order_by(Position.id_pos)
    )
    rows = db.session.execute(stmt).all()
    
    sql = stmt.compile(
    dialect=postgresql.dialect(),
    compile_kwargs={"literal_binds": True}
    )
    logger.info(sql)
    
    items = []
    for position, count in rows:
        items.append({
            "id_pos": position.id_pos,
            "name_pos": position.name_pos,
            "salary": position.salary,
            "emp_count": count,
        })
    return items