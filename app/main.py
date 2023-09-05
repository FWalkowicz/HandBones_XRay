from typing import Union
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from train import XRayPredictions
import cv2
import os

app = FastAPI()

XRayStorage = {
    "UniqueSessionId": str
}


@app.get("/")
def read_root():
    return {"Hello": "World"}


class Item(BaseModel):
    image: str
    description: Union[str, None] = None


@app.post("/executeAI")
def execute_ai(model: Item):
    processing = XRayPredictions(cv2.imread(os.path.join(os.getcwd(), "images/hand_no_good.jpg")))
    token = processing.start()
    XRayStorage['UniqueSessionId'] = token
    return {"UniqueSEssionId ": token}


@app.get("/sessions")
def sessions():
    result = []

    for dir_path, _, file_names in os.walk("./sessions"):
        if dir_path != "./sessions":
            session_dict = {
                "UniqueSessionId": os.path.basename(dir_path),
                "Files": []
            }

            for file_name in file_names:
                if file_name.endswith(".jpg"):
                    file_dict = {
                        "FileName": file_name[:-4],
                        "Type": "jpg"
                    }
                    session_dict["Files"].append(file_dict)

            result.append(session_dict)

    return result


@app.get("/session/{uniqueSessionId}")
def unique_session(uniqueSessionId: str):
    result = []

    for dir_path, _, file_names in os.walk(f"./sessions/{str(uniqueSessionId)}"):
        for file_name in file_names:
            if file_name.endswith(".jpg"):
                file_dict = {
                    "FileName": file_name[:-4],
                    "Type": "jpg"
                }
            result.append(file_dict)

    return result


@app.get("/session/{uniqueSessionId}/image/{fileName}")
def unique_session_image(uniqueSessionId: str, fileName: str):
    folder = uniqueSessionId
    file_name = fileName

    def file_iterator():
        with open(
            os.path.join(f"./sessions/{folder}", f"{file_name}.jpg"), mode="rb"
        ) as file:
            while True:
                chunk = file.read(65536)
                if not chunk:
                    break
                yield chunk

    return StreamingResponse(file_iterator(), media_type="application/octet-stream")


@app.get("/session/{uniqueSessionId}/meta/{fileName}")
def unique_session_meta():
    pass


@app.delete("/session/{uniqueSessionId}")
def delete_session():
    pass
