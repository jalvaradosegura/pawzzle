from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from pawzzle.assets import DATA_DIR_PATH
from pawzzle.db.init import init_db
from pawzzle.dependencies import get_session
from pawzzle.main import app


@pytest.fixture(name="session")
def session_fixture():
    engine = init_db(
        "sqlite:///:memory:",
        echo=False,  # type: ignore
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # type: ignore
    )
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="data_path")
def data_path_fixture() -> Path:
    return DATA_DIR_PATH
