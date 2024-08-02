from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from pawzzle.db.dog import insert_dog
from pawzzle.operations.schemas import (
    DogIn,
    QuestionIn,
    QuestionOut,
)


@pytest.fixture(name="question_base")
def question_base_fixture(session: Session) -> QuestionIn:
    dog_1 = insert_dog(session, "Poodle")
    dog_2 = insert_dog(session, "Pug")
    dog_3 = insert_dog(session, "Husky")
    dog_4 = insert_dog(session, "Corgi")
    insert_dog(session, "Samoyed")
    alternatives = [dog_1, dog_2, dog_3, dog_4]
    return QuestionIn(
        text="Which one is a Poodle",
        correct_dog=DogIn(**dog_1.to_dict()),
        alternatives=[DogIn(**dog.to_dict()) for dog in alternatives],
    )


@pytest.fixture(name="question_base")
def question_schema_fixture(question_base: QuestionIn) -> QuestionOut:
    return QuestionOut(id=None, **question_base.model_dump())


@patch("pawzzle.routers.question.operations.generate_random_question")
def test_get_random_question(
    mocked_generate_random_question: MagicMock,
    client: TestClient,
    question_base: QuestionOut,
):
    mocked_generate_random_question.return_value = question_base
    response = client.get("/question")

    assert response.status_code == 200
    assert response.json() == {
        "text": "Which one is a Poodle",
        "correct_dog": {
            "breed": "Poodle",
            "id": 1,
            "image_url": None,
            "info_url": None,
        },
        "alternatives": [
            {
                "breed": "Poodle",
                "id": 1,
                "image_url": None,
                "info_url": None,
            },
            {
                "breed": "Pug",
                "id": 2,
                "image_url": None,
                "info_url": None,
            },
            {
                "breed": "Husky",
                "id": 3,
                "image_url": None,
                "info_url": None,
            },
            {
                "breed": "Corgi",
                "id": 4,
                "image_url": None,
                "info_url": None,
            },
        ],
    }


def test_store_question(question_base: QuestionIn, client: TestClient):
    response = client.post("/question", json=question_base.model_dump())

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "text": "Which one is a Poodle",
        "correct_dog": {
            "breed": "Poodle",
            "id": 1,
            "image_url": None,
            "info_url": None,
        },
        "alternatives": [
            {
                "breed": "Poodle",
                "id": 1,
                "image_url": None,
                "info_url": None,
            },
            {
                "breed": "Pug",
                "id": 2,
                "image_url": None,
                "info_url": None,
            },
            {
                "breed": "Husky",
                "id": 3,
                "image_url": None,
                "info_url": None,
            },
            {
                "breed": "Corgi",
                "id": 4,
                "image_url": None,
                "info_url": None,
            },
        ],
    }
