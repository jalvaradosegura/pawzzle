from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from pawzzle import db, operations


@pytest.fixture(name="question_base")
def question_base_fixture(session: Session) -> operations.QuestionIn:
    dog_1 = db.insert_dog(session, "Poodle")
    dog_2 = db.insert_dog(session, "Pug")
    dog_3 = db.insert_dog(session, "Husky")
    dog_4 = db.insert_dog(session, "Corgi")
    db.insert_dog(session, "Samoyed")
    alternatives = [dog_1, dog_2, dog_3, dog_4]
    return operations.QuestionIn(
        text="Which one is a Poodle",
        correct_dog=operations.DogIn(**dog_1.to_dict()),
        alternatives=[operations.DogIn(**dog.to_dict()) for dog in alternatives],
    )


@pytest.fixture(name="question_schema")
def question_schema_fixture(
    question_base: operations.QuestionIn,
) -> operations.QuestionOut:
    return operations.QuestionOut(id=None, **question_base.model_dump())


@patch("pawzzle.routers.question.operations.generate_random_question")
def test_get_random_question(
    mocked_generate_random_question: MagicMock,
    client: TestClient,
    question_schema: operations.QuestionOut,
):
    mocked_generate_random_question.return_value = question_schema
    response = client.get("/question")

    assert response.status_code == 200
    assert response.json() == {
        "text": "Which one is a Poodle",
        "correct_dog": {
            "breed": "Poodle",
            "id": 1,
            "image_url": None,
            "img_name": None,
            "info_url": None,
        },
        "alternatives": [
            {
                "breed": "Poodle",
                "id": 1,
                "image_url": None,
                "img_name": None,
                "info_url": None,
            },
            {
                "breed": "Pug",
                "id": 2,
                "image_url": None,
                "img_name": None,
                "info_url": None,
            },
            {
                "breed": "Husky",
                "id": 3,
                "image_url": None,
                "img_name": None,
                "info_url": None,
            },
            {
                "breed": "Corgi",
                "id": 4,
                "image_url": None,
                "img_name": None,
                "info_url": None,
            },
        ],
    }


@patch("pawzzle.operations.question.generate_random_question")
def test_get_random_questions(
    mocked_generate_random_question: MagicMock,
    client: TestClient,
    question_schema: operations.QuestionOut,
):
    mocked_generate_random_question.return_value = question_schema
    response = client.get("/questions")

    assert response.status_code == 200
    assert len(response.json()) == 5
    assert response.json()[0]["text"] == "Which one is a Poodle"
    assert response.json()[1]["text"] == "Which one is a Poodle"
    assert response.json()[2]["text"] == "Which one is a Poodle"
    assert response.json()[3]["text"] == "Which one is a Poodle"
    assert response.json()[4]["text"] == "Which one is a Poodle"


def test_store_question(question_base: operations.QuestionIn, client: TestClient):
    response = client.post("/question", json=question_base.model_dump())

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "text": "Which one is a Poodle",
        "correct_dog": {
            "breed": "Poodle",
            "id": 1,
            "image_url": None,
            "img_name": None,
            "info_url": None,
        },
        "alternatives": [
            {
                "breed": "Poodle",
                "id": 1,
                "image_url": None,
                "img_name": None,
                "info_url": None,
            },
            {
                "breed": "Pug",
                "id": 2,
                "image_url": None,
                "img_name": None,
                "info_url": None,
            },
            {
                "breed": "Husky",
                "id": 3,
                "image_url": None,
                "img_name": None,
                "info_url": None,
            },
            {
                "breed": "Corgi",
                "id": 4,
                "image_url": None,
                "img_name": None,
                "info_url": None,
            },
        ],
    }


def test_store_questions(session: Session, client: TestClient):
    db.insert_dog(session, "Poodle")
    db.insert_dog(session, "Pug")
    db.insert_dog(session, "Husky")
    db.insert_dog(session, "Corgi")
    random_questions = operations.generate_random_questions(
        session, alternatives_amount=4, questions_amount=4
    )

    response = client.post(
        "/questions", json=[question.model_dump() for question in random_questions]
    )
    all_questions = db.select_all_questions(session)
    associations = session.query(db.question_dog_association).all()

    assert response.status_code == 201
    assert len(all_questions) == 4
    assert len(associations) == 16
