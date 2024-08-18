from typing import Any

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from pawzzle.db.models import Base
from pawzzle.settings import Settings


def get_engine(
    db_connection_url: str, *, echo: bool, **kwargs: dict[str, Any]
) -> Engine:
    engine = create_engine(db_connection_url, echo=echo, **kwargs)
    Base.metadata.create_all(engine)
    return engine


settings = Settings()
Session = sessionmaker(
    bind=get_engine(settings.db_connection_url, echo=settings.db_echo)
)
