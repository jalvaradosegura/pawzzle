import json
from typing import Any

from pawzzle.cache.types import Cache

ONE_DAY_IN_SECONDS = 86_400


def get_todays_quiz_if_cached(cache: Cache, todays_date: str):
    if todays_date in cache:
        cached = json.loads(cache.get(todays_date))  # type: ignore
        return cached

    return None


def store_todays_quiz_in_cache(
    cache: Cache, quiz: dict[str, Any], todays_date: str
) -> None:
    data = json.dumps(quiz)
    cache.set(todays_date, data, ONE_DAY_IN_SECONDS)
