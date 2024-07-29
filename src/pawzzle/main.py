from fastapi import FastAPI

from pawzzle.routers import question


app = FastAPI()
app.include_router(question.router)
