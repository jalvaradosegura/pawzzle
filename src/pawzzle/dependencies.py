from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from pawzzle.db.init import init_db
from pawzzle.settings import Settings


@lru_cache
def get_settings() -> Settings:  # pragma: no cover
    return Settings()


def get_session(settings: Settings = Depends(get_settings)):  # pragma: no cover
    engine, _ = init_db(
        settings.db_connection_url,
        echo=False,  # type: ignore
        connect_args={"check_same_thread": True},
        poolclass=StaticPool,  # type: ignore
    )
    with Session(engine) as session:
        yield session
