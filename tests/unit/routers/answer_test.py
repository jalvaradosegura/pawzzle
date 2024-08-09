import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from pawzzle import db, operations


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


@pytest.fixture(name="questions")
def questions_fixture(session: Session) -> list[db.Question]:
    poodle = db.insert_dog(session, "Poodle")
    pug = db.insert_dog(session, "Pug")
    question_1 = db.insert_question(
        session,
        text="Which one is a Poodle?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
    )
    question_2 = db.insert_question(
        session,
        text="Which one is a Pug?",
        alternatives=[poodle, pug],
        correct_dog=pug,
    )

    return [question_1, question_2]


def test_post_answer_correct(client: TestClient, question: db.Question):
    answer_in_schema = operations.AnswerIn(
        dog_id=2,
        question_id=question.id,
    )

    response = client.post("/answer", json=answer_in_schema.model_dump())

    assert response.status_code == 201
    assert response.json() == {"id": 1, "dog_id": 2, "question_id": 2, "correct": True}


def test_post_answers(
    client: TestClient, questions: list[db.Question], session: Session
):
    answer_in_schema_1 = operations.AnswerIn(
        dog_id=questions[0].alternatives[0].id, question_id=questions[0].id
    )
    answer_in_schema_2 = operations.AnswerIn(
        dog_id=questions[1].alternatives[1].id, question_id=questions[1].id
    )
    answers_in_schema = operations.AnswersIn(
        answers=[answer_in_schema_1, answer_in_schema_2]
    )

    response = client.post("/answers", json=answers_in_schema.model_dump())
    all_answers = session.query(db.Answer).all()

    assert response.status_code == 201
    assert len(all_answers) == 2
