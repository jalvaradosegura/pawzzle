import pytest
from fastapi.testclient import TestClient


from sqlalchemy.orm import Session

from pawzzle import db
from pawzzle import operations


@pytest.fixture(name="question")
def question_fixture(session: Session) -> db.Question:
    poodle = db.insert_dog(session, "Poodle")
    pug = db.insert_dog(session, "Pug")
    db.insert_question(
        session,
        text="Which one is a Poodle?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
    )
    question = db.insert_question(
        session,
        text="Which one is a Pug?",
        alternatives=[poodle, pug],
        correct_dog=pug,
    )

    return question


def test_store_answer_correct(client: TestClient, question: db.Question):
    schema = operations.AnswerIn(
        dog_id=2,
        question_id=question.id,
    )

    response = client.post("/answer", json=schema.model_dump())

    assert response.status_code == 201
    assert response.json() == {"id": 1, "dog_id": 2, "question_id": 2, "correct": True}
