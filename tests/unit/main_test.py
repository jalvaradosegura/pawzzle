import pytest
from fastapi.exceptions import HTTPException
from fastapi.testclient import TestClient


def test_middleware_fail(client: TestClient):
    del client.headers["api-key"]
    some_request = {
        "dog_id": 2,
        "question_id": 1,
    }

    with pytest.raises(HTTPException, match="401: You are not authorized"):
        client.post("/answer", json=some_request)
