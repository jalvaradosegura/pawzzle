import os
from datetime import datetime, timedelta

import requests

BACKEND_HOST = os.environ["BACKEND_HOST"]
ALTERNATIVES_MIN_AMOUNT = 3
ALTERNATIVES_MAX_AMOUNT = 5
QUESTIONS_PER_QUIZ = 10
YEAR = 2024


def get_questions(amount_of_days_in_year: int):
    response = requests.get(
        f"{BACKEND_HOST}/questions?questions_amount={QUESTIONS_PER_QUIZ * amount_of_days_in_year}&alternatives_amount=4",
        headers={"api-key": os.environ["API_KEY"]},
    )
    print(response)
    return response.json()


def loop_through_year(year: int):
    # Start with the first day of the year

    quizzes = []

    start_date = datetime(year, 1, 1)
    amount_of_days_in_year = 365 if not year % 4 == 0 else 366
    questions = get_questions(amount_of_days_in_year)

    # Loop through all days of the year
    idx = 0
    for i in range(amount_of_days_in_year):
        current_date = start_date + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")

        quizzes.append(
            {
                "target_date": date_str,
                "questions": questions[idx : idx + QUESTIONS_PER_QUIZ],
            }
        )
        idx += QUESTIONS_PER_QUIZ

    response = requests.post(
        f"{BACKEND_HOST}/quizzes",
        json=quizzes,
        headers={"api-key": os.environ["API_KEY"]},
    )
    print(response)


loop_through_year(YEAR)
