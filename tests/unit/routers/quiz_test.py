import random

import pytest
from pytest import MonkeyPatch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from pawzzle.db.dog import insert_dog
from pawzzle.db.models import Dog
from pawzzle.operations.schemas import QuestionIn
from pawzzle.operations.question import generate_random_question


@pytest.fixture(name="random_question", autouse=True)
def random_question_fixture(session: Session, monkeypatch: MonkeyPatch):
    dog_1 = insert_dog(session, "Poodle")
    dog_2 = insert_dog(session, "Pug")
    dog_3 = insert_dog(session, "Husky")
    random.seed(1)

    def mocked_randomly_get_n_dogs(
        alternatives_amount: int, session: Session
    ) -> list[Dog]:
        return [dog_1, dog_2, dog_3]

    monkeypatch.setattr(
        "pawzzle.operations.question.randomly_select_n_dogs",
        mocked_randomly_get_n_dogs,
    )


@pytest.fixture(name="list_of_questions")
def list_of_questions_fixture(session: Session) -> list[QuestionIn]:
    question_1 = generate_random_question(session, alternatives_amount=2)
    question_2 = generate_random_question(session, alternatives_amount=2)
    return [question_1, question_2]


def test_post_quiz(client: TestClient, list_of_questions: list[QuestionIn]):
    response = client.post(
        "/quiz", json=[question.model_dump() for question in list_of_questions]
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "questions": [
            {
                "text": "Which one is a Poodle",
                "correct_dog": {
                    "id": 1,
                    "breed": "Poodle",
                    "image_url": None,
                    "info_url": None,
                },
                "alternatives": [
                    {"id": 1, "breed": "Poodle", "image_url": None, "info_url": None},
                    {"id": 2, "breed": "Pug", "image_url": None, "info_url": None},
                    {"id": 3, "breed": "Husky", "image_url": None, "info_url": None},
                ],
                "id": None,
            },
            {
                "text": "Which one is a Husky",
                "correct_dog": {
                    "id": 3,
                    "breed": "Husky",
                    "image_url": None,
                    "info_url": None,
                },
                "alternatives": [
                    {"id": 1, "breed": "Poodle", "image_url": None, "info_url": None},
                    {"id": 2, "breed": "Pug", "image_url": None, "info_url": None},
                    {"id": 3, "breed": "Husky", "image_url": None, "info_url": None},
                ],
                "id": None,
            },
        ],
    }
