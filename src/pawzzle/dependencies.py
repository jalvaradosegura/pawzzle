from functools import lru_cache

from pawzzle.db.init import Session
from pawzzle.settings import Settings


@lru_cache
def get_settings() -> Settings:  # pragma: no cover
    return Settings()


def get_session():  # pragma: no cover
    with Session() as session:
        yield session
