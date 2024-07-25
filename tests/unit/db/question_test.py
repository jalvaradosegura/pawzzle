from sqlalchemy.orm import Session

from pawzzle.db.dog import store_dog
from pawzzle.db.question import get_all_questions, get_question, store_question


def test_store_question(session: Session):
    poodle = store_dog("Poodle", session)
    pug = store_dog("Pug", session)

    question = store_question(
        "Which one is a Poodle?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
        session=session,
    )

    assert question.id == 1
    assert question.text == "Which one is a Poodle?"
    assert question.alternatives == [poodle, pug]
    assert question.correct_dog == poodle


def test_get_question(session: Session):
    poodle = store_dog("Poodle", session)
    pug = store_dog("Pug", session)
    store_question(
        "Which one is a Poodle?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
        session=session,
    )

    question = get_question(1, session)

    assert question.id == 1
    assert question.text == "Which one is a Poodle?"
    assert question.alternatives == [poodle, pug]
    assert question.correct_dog == poodle


def test_get_all_questions(session: Session):
    poodle = store_dog("Poodle", session)
    pug = store_dog("Pug", session)
    store_question(
        "Which one is a Poodle?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
        session=session,
    )
    store_question(
        "Which one is a Pug?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
        session=session,
    )

    questions = get_all_questions(session)

    assert len(questions) == 2
    assert questions[0].id == 1
    assert questions[0].text == "Which one is a Poodle?"
    assert questions[0].alternatives == [poodle, pug]
    assert questions[0].correct_dog == poodle


def test_get_all_questions_limit(session: Session):
    poodle = store_dog("Poodle", session)
    pug = store_dog("Pug", session)
    store_question(
        "Which one is a Poodle?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
        session=session,
    )
    store_question(
        "Which one is a Pug?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
        session=session,
    )

    questions = get_all_questions(session, limit=1)

    assert len(questions) == 1
    assert questions[0].id == 1
    assert questions[0].text == "Which one is a Poodle?"
    assert questions[0].alternatives == [poodle, pug]
    assert questions[0].correct_dog == poodle


def test_get_all_questions_offset(session: Session):
    poodle = store_dog("Poodle", session)
    pug = store_dog("Pug", session)
    store_question(
        "Which one is a Poodle?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
        session=session,
    )
    store_question(
        "Which one is a Pug?",
        alternatives=[poodle, pug],
        correct_dog=pug,
        session=session,
    )

    questions = get_all_questions(session, offset=1)

    assert len(questions) == 1
    assert questions[0].id == 2
    assert questions[0].text == "Which one is a Pug?"
    assert questions[0].alternatives == [poodle, pug]
    assert questions[0].correct_dog == pug


def test_get_all_questions_limit_and_offset(session: Session):
    poodle = store_dog("Poodle", session)
    pug = store_dog("Pug", session)
    store_question(
        "Which one is a Poodle?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
        session=session,
    )
    store_question(
        "I'm a wrong question, but stored anyway",
        alternatives=[poodle, pug],
        correct_dog=pug,
        session=session,
    )
    store_question(
        "Which one is a Pug?",
        alternatives=[poodle, pug],
        correct_dog=pug,
        session=session,
    )

    questions = get_all_questions(session, limit=1, offset=1)

    assert len(questions) == 1
    assert questions[0].id == 2
    assert questions[0].text == "I'm a wrong question, but stored anyway"
