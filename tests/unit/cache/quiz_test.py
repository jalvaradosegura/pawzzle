from sqlalchemy.orm import Session
from pawzzle.cache.quiz import get_todays_quiz_if_cached, store_todays_quiz_in_cache
from pawzzle.operations import generate_random_quiz
from tests.fakes.cache import CacheFake


def test_get_todays_quiz_if_cached_not_cached():
    cache = CacheFake()
    result = get_todays_quiz_if_cached(cache, "2024-08-23")
    assert result is None


def test_get_todays_quiz_if_cached_cached(session: Session):
    cache = CacheFake()
    quiz = generate_random_quiz(
        session, questions_amount=2, target_date=""
    )  # this will create an empty quiz
    store_todays_quiz_in_cache(cache, quiz.model_dump(), "2024-08-23")

    result = get_todays_quiz_if_cached(cache, "2024-08-23")

    assert result == {"questions": [], "target_date": ""}
