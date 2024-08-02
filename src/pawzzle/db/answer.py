from sqlalchemy.orm import Session

from pawzzle.db.models import Answer


def insert_answer(
    *, dog_id: int, correct: bool, question_id: int, session: Session
) -> Answer:
    answer = Answer(correct=correct, question_id=question_id, dog_id=dog_id)
    session.add(answer)
    session.commit()
    return answer
