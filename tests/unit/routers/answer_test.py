import pytest
from fastapi.testclient import TestClient


from sqlalchemy.orm import Session

from pawzzle.db.dog import insert_dog
from pawzzle.db.models import Question
from pawzzle.db.question import insert_question
from pawzzle.operations.schemas import AnswerIn


@pytest.fixture(name="question")
def question_fixture(session: Session) -> Question:
    poodle = insert_dog(session, "Poodle")
    pug = insert_dog(session, "Pug")
    insert_question(
        session,
        text="Which one is a Poodle?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
    )
    question = insert_question(
        session,
        text="Which one is a Pug?",
        alternatives=[poodle, pug],
        correct_dog=pug,
    )

    return question


def test_store_answer_correct(client: TestClient, question: Question):
    schema = AnswerIn(
        dog_id=2,
        question_id=question.id,
    )

    response = client.post("/answer", json=schema.model_dump())

    assert response.status_code == 201
    assert response.json() == {"id": 1, "dog_id": 2, "question_id": 2, "correct": True}
