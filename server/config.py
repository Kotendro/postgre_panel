from pathlib import Path
from dataclasses import dataclass
from environs import Env

@dataclass
class DatabaseConfig:
    CONTAINER_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    PORT: int
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
            CONTAINER_NAME=env("CONTAINER_NAME"),
            POSTGRES_USER=env("POSTGRES_USER"),
            POSTGRES_PASSWORD=env("POSTGRES_PASSWORD"),
            POSTGRES_DB=env("POSTGRES_DB"),
            PORT=env("PORT"),
            DATABASE_URI=(
                f"postgresql://{env('POSTGRES_USER')}:"
                f"{env('POSTGRES_PASSWORD')}@localhost:"
                f"{env('PORT')}/{env('POSTGRES_DB')}"
            ),
        ),
        var=Var(
            PER_PAGE=20
        )
    )
    return config