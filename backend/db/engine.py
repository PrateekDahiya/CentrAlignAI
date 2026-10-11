"""SQLAlchemy engine with Aiven MySQL SSL."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.config import settings
from backend.utils.logging import inside


def build_url() -> str:
    inside("build_url", settings.db_name)
    return (
        f"mysql+pymysql://{settings.db_user}:{settings.db_password}"
        f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    )


def create_engine_ssl():
    inside("create_engine_ssl", settings.db_host)
    connect_args = {"ssl": {"ssl": True}} if settings.db_ssl else {}
    return create_engine(build_url(), connect_args=connect_args, pool_pre_ping=True)


engine = create_engine_ssl()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
