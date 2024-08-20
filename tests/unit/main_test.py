from fastapi import status
from fastapi.testclient import TestClient


def test_middleware_fail(client: TestClient):
    del client.headers["api-key"]
    some_request = {
        "dog_id": 2,
        "question_id": 1,
    }

    response = client.post("/answer", json=some_request)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "You are not authorized"}
