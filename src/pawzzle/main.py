from contextlib import asynccontextmanager

from fastapi import FastAPI

from pawzzle.db.init import init_db
from pawzzle.routers import question
from pawzzle.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    settings = Settings()
    init_db(settings.db_connection_url)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(question.router)
