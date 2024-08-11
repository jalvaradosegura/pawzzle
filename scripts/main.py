import os
import random
from typing import Any
from datetime import datetime, timedelta

import requests

BACKEND_HOST = os.environ["BACKEND_HOST"]
ALTERNATIVES_MIN_AMOUNT = 3
ALTERNATIVES_MAX_AMOUNT = 5
YEAR = 2024


def get_questions():
    alternatives_amount = random.randint(
        ALTERNATIVES_MIN_AMOUNT, ALTERNATIVES_MAX_AMOUNT
    )
    response = requests.get(
        f"{BACKEND_HOST}/questions?questions_amount=10&alternatives_amount={alternatives_amount}",
        headers={"api-key": os.environ["API_KEY"]},
    )
    return response.json()


def create_quiz(target_date: str, questions: Any):
    response = requests.post(
        f"{BACKEND_HOST}/quiz",
        json={"target_date": target_date, "questions": questions},
        headers={"api-key": os.environ["API_KEY"]},
    )
    print(response)


def loop_through_year(year: int):
    # Start with the first day of the year
    start_date = datetime(year, 1, 1)

    # Loop through all days of the year
    for i in range(365 if not year % 4 == 0 else 366):
        current_date = start_date + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")
        questions = get_questions()
        create_quiz(date_str, questions)


loop_through_year(YEAR)
