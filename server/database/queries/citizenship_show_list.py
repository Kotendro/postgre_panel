from sqlalchemy.dialects import postgresql
from ..models import Citizenship, Report, Employee
from .. import db
from logging import getLogger

logger = getLogger(__name__)

def get_citizenship_show_list():
    items = None

    stmt = (
        db.select(
            Citizenship,
            db.func.count(Employee.id_emp).label("emp_count")
        )
        .outerjoin(
            Employee,
            Citizenship.id_cit == Employee.id_cit    
        )
        .group_by(Citizenship.id_cit)
        .order_by(Citizenship.id_cit)
    )
    
    rows = db.session.execute(stmt).all()
    
    sql = stmt.compile(
    dialect=postgresql.dialect(),
    compile_kwargs={"literal_binds": True}
    )
    logger.info(sql)
    
    items = []
    for citizenship, count in rows:
        items.append({
            "id_cit": citizenship.id_cit,
            "name_cit": citizenship.name_cit,
            "emp_count": count,
        })
    
    return items