import os
from fastapi import FastAPI

app = FastAPI()

APP_ENV = os.getenv("APP_ENV", "dev")


@app.get("/hello")
def hello():
    return {"message": "Hello World", "env": APP_ENV}


@app.get("/health")
def health():
    return {"status": "ok"}
