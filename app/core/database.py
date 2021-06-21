from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager
from core.config import settings


Base = declarative_base()


class Database:

    def __init__(self) -> None:
        self._engine = create_engine(
            settings.SQLALCHEMY_DATABASE_URI,
            pool_pre_ping=True
        )
        self._session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self):
        session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


db = Database()
