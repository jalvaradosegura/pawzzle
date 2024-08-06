from sqlalchemy.orm import Session
from pawzzle import db
from pawzzle.operations.schemas import QuestionIn, QuestionOut, QuizOut


def store_quiz(session: Session, list_of_questions: list[QuestionIn]) -> QuizOut:
    questions_to_bulk: list[db.BulkQuestionData] = [
        {
            "text": question.text,
            "alternatives": [alternative.id for alternative in question.alternatives],
            "correct_dog_id": question.correct_dog.id,
        }
        for question in list_of_questions
    ]
    questions_id = db.bulk_insert_questions(session, questions_to_bulk)
    questions = db.select_all_questions(session, filter_=questions_id)
    quiz = db.insert_quiz(session, questions)

    return QuizOut(
        id=quiz.id,
        questions=[QuestionOut(**q.to_dict()) for q in quiz.questions],
    )
