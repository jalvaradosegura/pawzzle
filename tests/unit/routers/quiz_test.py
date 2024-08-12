import random
from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import pytest
from fastapi.testclient import TestClient
from pytest import MonkeyPatch
from sqlalchemy.orm import Session

from pawzzle import db
from pawzzle.operations.question import generate_random_question
from pawzzle.operations.schemas import QuestionIn, QuizIn


@pytest.fixture(name="random_question", autouse=True)
def random_question_fixture(session: Session, monkeypatch: MonkeyPatch):
    dog_1 = db.insert_dog(session, "Poodle")
    dog_2 = db.insert_dog(session, "Pug")
    dog_3 = db.insert_dog(session, "Husky")
    random.seed(1)

    def mocked_randomly_get_n_dogs(
        alternatives_amount: int, session: Session
    ) -> list[db.Dog]:
        return [dog_1, dog_2, dog_3]

    monkeypatch.setattr(
        "pawzzle.operations.question.db.randomly_select_n_dogs",
        mocked_randomly_get_n_dogs,
    )


@pytest.fixture(name="list_of_questions")
def list_of_questions_fixture(session: Session) -> list[QuestionIn]:
    question_1 = generate_random_question(session, alternatives_amount=2)
    question_2 = generate_random_question(session, alternatives_amount=2)
    return [question_1, question_2]


def test_post_quiz(client: TestClient, list_of_questions: list[QuestionIn]):
    quiz_in = QuizIn(target_date="2024-08-23", questions=list_of_questions)
    response = client.post("/quiz", json=quiz_in.model_dump())
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "target_date": "2024-08-23",
        "questions": [
            {
                "text": "Which one is a Poodle",
                "correct_dog": {
                    "id": 1,
                    "breed": "Poodle",
                    "img_name": None,
                    "info_url": None,
                },
                "alternatives": [
                    {
                        "id": 1,
                        "breed": "Poodle",
                        "img_name": None,
                        "info_url": None,
                    },
                    {
                        "id": 2,
                        "breed": "Pug",
                        "img_name": None,
                        "info_url": None,
                    },
                    {
                        "id": 3,
                        "breed": "Husky",
                        "img_name": None,
                        "info_url": None,
                    },
                ],
                "id": 1,
            },
            {
                "text": "Which one is a Husky",
                "correct_dog": {
                    "id": 3,
                    "breed": "Husky",
                    "img_name": None,
                    "info_url": None,
                },
                "alternatives": [
                    {
                        "id": 1,
                        "breed": "Poodle",
                        "img_name": None,
                        "info_url": None,
                    },
                    {
                        "id": 2,
                        "breed": "Pug",
                        "img_name": None,
                        "info_url": None,
                    },
                    {
                        "id": 3,
                        "breed": "Husky",
                        "img_name": None,
                        "info_url": None,
                    },
                ],
                "id": 2,
            },
        ],
    }


def test_get_quiz(client: TestClient, list_of_questions: list[QuestionIn]):
    quiz_in = QuizIn(target_date="2024-08-23", questions=list_of_questions)
    client.post("/quiz", json=quiz_in.model_dump())

    response = client.get("/quiz/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert len(response.json()["questions"]) == 2
    assert len(response.json()["questions"][0]["alternatives"]) == 3


def test_post_quizzes(client: TestClient, list_of_questions: list[QuestionIn]):
    quiz_in_1 = QuizIn(target_date="2024-08-23", questions=list_of_questions)
    quiz_in_2 = QuizIn(target_date="2024-08-24", questions=list_of_questions)
    client.post("/quizzes", json=[quiz_in_1.model_dump(), quiz_in_2.model_dump()])

    response_1 = client.get("/quiz/1")
    response_2 = client.get("/quiz/2")

    assert response_1.status_code == 200
    assert response_2.status_code == 200
    assert response_1.json()["id"] == 1
    assert response_2.json()["id"] == 2
    assert len(response_1.json()["questions"]) == 2
    assert len(response_2.json()["questions"]) == 2
    assert len(response_1.json()["questions"][0]["alternatives"]) == 3
    assert len(response_2.json()["questions"][0]["alternatives"]) == 3


@patch("pawzzle.operations.quiz.datetime")
def test_get_todays_quiz(
    mocked_datetime_now: MagicMock,
    client: TestClient,
    list_of_questions: list[QuestionIn],
):
    mocked_datetime_now.now = Mock(return_value=datetime(2024, 8, 23))
    quiz_in = QuizIn(target_date="2024-08-23", questions=list_of_questions)
    client.post("/quiz", json=quiz_in.model_dump())

    response = client.get("/quiz")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert len(response.json()["questions"]) == 2
    assert len(response.json()["questions"][0]["alternatives"]) == 3
