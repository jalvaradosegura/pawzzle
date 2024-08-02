from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.orm import Session

from pawzzle.assets import DATA_DIR_PATH
from pawzzle.db.init import init_db
from pawzzle.operations.dog import seed_dog_table
from pawzzle.routers import answer, question
from pawzzle.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    settings = Settings()
    engine = init_db(settings.db_connection_url, echo=settings.db_echo)  # type: ignore
    with Session(engine) as session:
        seed_dog_table(session, DATA_DIR_PATH / settings.dogs_file)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(question.router)
app.include_router(answer.router)
