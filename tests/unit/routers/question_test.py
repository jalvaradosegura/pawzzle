from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from pawzzle.db.dog import insert_dog
from pawzzle.operations.schemas import (
    DogSchema,
    QuestionSchema,
    QuestionWithIDSchema,
)


@pytest.fixture(name="question_base")
def question_base_fixture(session: Session) -> QuestionSchema:
    dog_1 = insert_dog("Poodle", session)
    dog_2 = insert_dog("Pug", session)
    dog_3 = insert_dog("Husky", session)
    dog_4 = insert_dog("Corgi", session)
    insert_dog("Samoyed", session)
    alternatives = [dog_1, dog_2, dog_3, dog_4]
    return QuestionSchema(
        text="Which one is a Poodle",
        correct_dog=DogSchema(**dog_1.to_dict()),
        alternatives=[DogSchema(**dog.to_dict()) for dog in alternatives],
    )


@pytest.fixture(name="question_base")
def question_schema_fixture(question_base: QuestionSchema) -> QuestionWithIDSchema:
    return QuestionWithIDSchema(id=None, **question_base.model_dump())


@patch("pawzzle.routers.question.operations.generate_random_question")
def test_get_random_question(
    mocked_generate_random_question: MagicMock,
    client: TestClient,
    question_base: QuestionWithIDSchema,
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


def test_store_question(question_base: QuestionSchema, client: TestClient):
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
