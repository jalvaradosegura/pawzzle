import os
from collections.abc import Callable
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any

import sentry_sdk
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from pawzzle.assets import DATA_DIR_PATH
from pawzzle.db.init import init_db
from pawzzle.operations.dog import seed_dog_table
from pawzzle.operations.question import seed_question_table
from pawzzle.operations.quiz import seed_quiz_table
from pawzzle.routers import answer, question, quiz
from pawzzle.settings import Settings


settings = Settings()
origins = [*settings.origins.split(",")]


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover

    engine = init_db(settings.db_connection_url, echo=settings.db_echo)  # type: ignore
    with Session(engine) as session:
        seed_dog_table(session, DATA_DIR_PATH / settings.dogs_file)
        seed_question_table(session, questions_amount=5000, alternatives_amount=4)
        seed_quiz_table(session, year=datetime.now().year)
    yield


if os.environ.get("IS_TEST", None) != "True":  # pragma: no cover
    sentry_sdk.init(
        dsn=settings.sentry_dns,
        environment=settings.sentry_environment,
        traces_sample_rate=settings.sentry_traces_sample_rate,
        profiles_sample_rate=settings.sentry_profiles_sample_rate,
    )


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"]
)
app.include_router(answer.router)
app.include_router(quiz.router)
app.include_router(question.router)


@app.middleware("http")
async def authenticate_request(request: Request, call_next: Callable[[Request], Any]):
    if (
        "api-key" not in request.headers
        or request.headers["api-key"] != settings.api_key
    ):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You are not authorized")

    response = await call_next(request)
    return response
