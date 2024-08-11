from sqlalchemy.orm import Session

from pawzzle import db
from pawzzle.operations.schemas import QuestionOut, QuizIn, QuizOut


def store_quiz(session: Session, quiz_in: QuizIn) -> QuizOut:
    questions_to_bulk: list[db.BulkQuestionData] = [
        {
            "text": question.text,
            "alternatives": [alternative.id for alternative in question.alternatives],
            "correct_dog_id": question.correct_dog.id,
        }
        for question in quiz_in.questions
    ]
    questions_id = db.bulk_insert_questions(session, questions_to_bulk)
    questions = db.select_all_questions(session, filter_=questions_id)
    quiz = db.insert_quiz(session, questions, quiz_in.target_date)

    return QuizOut(
        id=quiz.id,
        questions=[QuestionOut(**q.to_dict()) for q in quiz.questions],
        target_date=quiz_in.target_date,
    )


def get_quiz(session: Session, id: int):
    quiz = db.select_quiz(session, id)
    return QuizOut(
        id=quiz.id,
        questions=[QuestionOut(**q.to_dict()) for q in quiz.questions],
        target_date=quiz.target_date,
    )
