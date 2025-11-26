from pathlib import Path
from dataclasses import dataclass
from environs import Env

@dataclass
class DatabaseConfig:
    DATABASE_URI: str

@dataclass
class FlaskConfig:
    PROJECT_DIR: Path
    SERVER_DIR: Path
    CLIENT_DIR: Path
    TEMPLATES_DIR: Path
    STATIC_DIR: Path
    UPLOADS_DIR: Path
    SECRET_KEY: str

@dataclass()
class Var:
    """Variable  data"""
    PER_PAGE: int

@dataclass()
class Config:
    db: DatabaseConfig
    flask: FlaskConfig
    var: Var

def load_config():
    env = Env()
    env.read_env()
    
    PROJECT_DIR=Path.cwd()
    config = Config(
        flask=FlaskConfig(
            PROJECT_DIR=PROJECT_DIR,
            SERVER_DIR=PROJECT_DIR / "server",
            CLIENT_DIR=PROJECT_DIR / "client",
            TEMPLATES_DIR=PROJECT_DIR / "client" / "templates",
            STATIC_DIR=PROJECT_DIR / "client" / "static",
            UPLOADS_DIR=PROJECT_DIR / "uploads",
            SECRET_KEY=env("SECRET_KEY")
        ),
        db=DatabaseConfig(
            DATABASE_URI = f"sqlite:///{PROJECT_DIR / "server" / "database" / "register.db"}"
        ),
        var=Var(
            PER_PAGE=20
        )
    )
    return config