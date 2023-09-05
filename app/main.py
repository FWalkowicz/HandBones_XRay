from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/executeAI")
def execute_ai():
    pass


@app.get("/sessions")
def sessions():
    pass


@app.get("/session/{uniqueSessionId}")
def unique_session():
    pass


@app.get("/session/{uniqueSessionId}/image/{fileName}")
def unique_session_image():
    pass


@app.get("/session/{uniqueSessionId}/meta/{fileName}")
def unique_session_meta():
    pass


@app.delete("/session/{uniqueSessionId}")
def delete_session():
    pass
