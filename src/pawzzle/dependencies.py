from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from pawzzle.db.init import init_db
from pawzzle.settings import Settings


@lru_cache
def get_settings() -> Settings:  # pragma: no cover
    return Settings()


def get_session(settings: Settings = Depends(get_settings)):  # pragma: no cover
    engine = init_db(settings.db_connection_url)
    with Session(engine) as session:
        yield session
