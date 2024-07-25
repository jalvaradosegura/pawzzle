import pytest
from sqlalchemy.orm import Session

from pawzzle.db.init import init_db


@pytest.fixture(name="session")
def session_fixture():
    engine, Base = init_db("sqlite:///:memory:", echo=True)  # type: ignore
    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)
