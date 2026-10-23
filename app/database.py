
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = "sqlite:///expense_tracker.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


@event.listens_for(engine, "connect")
def enable_foreign_keys(connection, _record):
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def create_tables():
    from app import models  # Register the models
    Base.metadata.create_all(engine)
