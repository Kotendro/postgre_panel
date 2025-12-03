from sqlalchemy.dialects import postgresql
from ..models import Education, Report, Employee
from .. import db
from logging import getLogger

logger = getLogger(__name__)

def get_education_show_list():
    items = None

    stmt = (
        db.select(
            Education,
            db.func.count(Employee.id_emp).label("emp_count")
        )
        .outerjoin(
            Employee,
            Education.id_edu == Employee.id_edu    
        )
        .group_by(Education.id_edu)
        .order_by(Education.id_edu)
    )
    
    rows = db.session.execute(stmt).all()
    
    sql = stmt.compile(
    dialect=postgresql.dialect(),
    compile_kwargs={"literal_binds": True}
    )
    logger.info(sql)
    
    items = []
    for education, count in rows:
        items.append({
            "id_edu": education.id_edu,
            "name_edu": education.name_edu,
            "emp_count": count,
        })
    
    return items