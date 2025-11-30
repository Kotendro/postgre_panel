from .home import core as home_bp
from .employee import core as employee_bp
from .citizenship import core as citizenship_bp
from .education import core as education_bp
from .division import core as division_bp
from .position import core as position_bp
from .report import core as report_bp

ALL_BLUEPRINTS = (
    home_bp,
    employee_bp,
    citizenship_bp,
    education_bp,
    division_bp,
    position_bp,
    report_bp
)

def register_blueprints(app):
    for bp in ALL_BLUEPRINTS:
        app.register_blueprint(bp)
