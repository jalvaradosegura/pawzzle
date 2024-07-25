from typing import Any
from sqlalchemy import create_engine, Engine

from pawzzle.db.models import Base


def init_db(
    db_connection_url: str, **kwargs: dict[str, Any]
) -> tuple[Engine, type[Base]]:
    engine = create_engine(db_connection_url, **kwargs)
    Base.metadata.create_all(engine)
    return engine, Base
