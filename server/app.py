from flask import Flask
from .config import load_config, Config
from .routes import core
from .database import db

def create_app() -> Flask:
    config: Config = load_config()

    app = Flask(
        __name__,
        template_folder=config.flask.TEMPLATES_DIR,
        static_folder=config.flask.STATIC_DIR,
    )

    app.config['SECRET_KEY'] = config.flask.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = config.db.DATABASE_URI

    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    app.register_blueprint(core)
    
    return app

def run():
    app = create_app()
    app.run(debug=True)