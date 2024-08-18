from functools import lru_cache

from fastapi import Request
from sqlalchemy.orm import Session

from pawzzle.cache.types import Cache
from pawzzle.db.init import Session
from pawzzle.settings import Settings


@lru_cache
def get_settings() -> Settings:  # pragma: no cover
    return Settings()


def get_session():  # pragma: no cover
    with Session() as session:
        yield session


def get_cache(request: Request) -> Cache:  # pragma: no cover
    return request.app.state.cache
