from sqlalchemy.orm import Session

from pawzzle.db.dog import insert_dog
from pawzzle.db.question import select_all_questions, select_question, insert_question


def test_insert_question(session: Session):
    poodle = insert_dog(session, "Poodle")
    pug = insert_dog(session, "Pug")

    question = insert_question(
        session,
        text="Which one is a Poodle?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
    )

    assert question.id == 1
    assert question.text == "Which one is a Poodle?"
    assert question.alternatives == [poodle, pug]
    assert question.correct_dog == poodle


def test_select_question(session: Session):
    poodle = insert_dog(session, "Poodle")
    pug = insert_dog(session, "Pug")
    insert_question(
        session,
        text="Which one is a Poodle?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
    )

    question = select_question(session, 1)

    assert question.id == 1
    assert question.text == "Which one is a Poodle?"
    assert question.alternatives == [poodle, pug]
    assert question.correct_dog == poodle


def test_select_all_questions(session: Session):
    poodle = insert_dog(session, "Poodle")
    pug = insert_dog(session, "Pug")
    insert_question(
        session,
        text="Which one is a Poodle?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
    )
    insert_question(
        session,
        text="Which one is a Pug?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
    )

    questions = select_all_questions(session)

    assert len(questions) == 2
    assert questions[0].id == 1
    assert questions[0].text == "Which one is a Poodle?"
    assert questions[0].alternatives == [poodle, pug]
    assert questions[0].correct_dog == poodle


def test_select_all_questions_limit(session: Session):
    poodle = insert_dog(session, "Poodle")
    pug = insert_dog(session, "Pug")
    insert_question(
        session,
        text="Which one is a Poodle?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
    )
    insert_question(
        session,
        text="Which one is a Pug?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
    )

    questions = select_all_questions(session, limit=1)

    assert len(questions) == 1
    assert questions[0].id == 1
    assert questions[0].text == "Which one is a Poodle?"
    assert questions[0].alternatives == [poodle, pug]
    assert questions[0].correct_dog == poodle


def test_select_all_questions_offset(session: Session):
    poodle = insert_dog(session, "Poodle")
    pug = insert_dog(session, "Pug")
    insert_question(
        session,
        text="Which one is a Poodle?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
    )
    insert_question(
        session,
        text="Which one is a Pug?",
        alternatives=[poodle, pug],
        correct_dog=pug,
    )

    questions = select_all_questions(session, offset=1)

    assert len(questions) == 1
    assert questions[0].id == 2
    assert questions[0].text == "Which one is a Pug?"
    assert questions[0].alternatives == [poodle, pug]
    assert questions[0].correct_dog == pug


def test_select_all_questions_limit_and_offset(session: Session):
    poodle = insert_dog(session, "Poodle")
    pug = insert_dog(session, "Pug")
    insert_question(
        session,
        text="Which one is a Poodle?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
    )
    insert_question(
        session,
        text="I'm a wrong question, but stored anyway",
        alternatives=[poodle, pug],
        correct_dog=pug,
    )
    insert_question(
        session,
        text="Which one is a Pug?",
        alternatives=[poodle, pug],
        correct_dog=pug,
    )

    questions = select_all_questions(session, limit=1, offset=1)

    assert len(questions) == 1
    assert questions[0].id == 2
    assert questions[0].text == "I'm a wrong question, but stored anyway"
