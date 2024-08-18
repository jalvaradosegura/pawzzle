from pathlib import Path

import pytest
from pytest import MonkeyPatch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from pawzzle.assets import DATA_DIR_PATH
from pawzzle.db.init import get_engine
from pawzzle.dependencies import get_cache, get_session
from pawzzle.main import app
from pawzzle.settings import Settings
from tests.fakes.cache import CacheFake


@pytest.fixture(name="session")
def session_fixture():
    engine = get_engine(
        "sqlite:///:memory:",
        echo=False,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # type: ignore
    )
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session, monkeypatch: MonkeyPatch):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    def get_cache_override():
        return CacheFake()

    app.dependency_overrides[get_cache] = get_cache_override

    client = TestClient(app)

    settings = Settings()
    client.headers.update({"api-key": settings.api_key})

    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="data_path")
def data_path_fixture() -> Path:
    return DATA_DIR_PATH
