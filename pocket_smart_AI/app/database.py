from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    """

    pass


# SQLite requires this option when used with FastAPI.
connect_args = {}

if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}


engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    future=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def create_tables() -> None:
    """
    Create all database tables.
    """
    # Import models here so SQLAlchemy knows about them
    # before create_all() is called.
    from app.models.history import History
    from app.models.planner import Planner
    from app.models.user import User

    # Avoid unused-import warnings.
    _ = (User, Planner, History)

    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI database dependency.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()