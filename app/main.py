from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import shutil
from pydantic import BaseModel
from train import XRayPredictions
import cv2
import os

app = FastAPI()

XRayStorage = {
    "UniqueSessionId": None,
    "Files": []
}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/executeAI")
async def execute_ai(input_image: UploadFile):
    """
    Execute AI processing on an uploaded X-ray image.

    :param input_image: The X-ray image file to be processed (JPEG or PNG).
    :return: Information about the processed session
    """
    if not input_image.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        return {"error": "Only JPEG and PNG images are supported."}

    # Save the uploaded file to a temporary location
    file_path = os.path.join("temp", input_image.filename)
    with open(file_path, "wb") as file:
        file.write(input_image.file.read())
    name = input_image.filename
    image = cv2.imread(file_path)
    os.remove(file_path)

    processing = XRayPredictions(image=image, filename=name)
    token = processing.start()
    XRayStorage['UniqueSessionId'] = token
    result = []

    for dir_path, _, file_names in os.walk(f"./sessions/{XRayStorage['UniqueSessionId']}"):
        for file_name in file_names:
            if file_name.endswith(".jpg"):
                file_dict = {
                    "FileName": file_name,
                    "Type": "Image"
                }
            if file_name.endswith(".txt"):
                file_dict = {
                    "FileName": file_name,
                    "Type": "Metadata"
                }

            result.append(file_dict)
    XRayStorage["Files"] = result
    return XRayStorage


@app.get("/sessions")
def sessions():
    """
    List all available sessions along with their associated files.

    :return: List of sessions, each containing session information and associated files.
    """
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
                        "FileName": file_name,
                        "Type": "Image"
                    }

                if file_name.endswith(".txt"):
                    file_dict = {
                        "FileName": file_name,
                        "Type": "Metadata"
                    }

                session_dict["Files"].append(file_dict)

            result.append(session_dict)

    return result


@app.get("/session/{unique_session_id}")
def unique_session(unique_session_id: str):
    """
    List files associated with a current session.

    :return: List of files within the current session.
    """
    result = []

    for dir_path, _, file_names in os.walk(f"./sessions/{unique_session_id}"):
        for file_name in file_names:
            if file_name.endswith(".jpg"):
                file_dict = {
                    "FileName": file_name,
                    "Type": "Image"
                }

            if file_name.endswith(".txt"):
                file_dict = {
                    "FileName": file_name,
                    "Type": "Metadata"
                }

            result.append(file_dict)

    return result


@app.get("/session/{unique_session_id}/image/{file_name}")
def unique_session_image(unique_session_id: str, file_name: str):
    """
    Stream an X-ray image file from a specific session.

    :return:
    """
    def file_iterator():
        with open(
            os.path.join(f"./sessions/{unique_session_id}/", f"{file_name}.jpg"), mode="rb"
        ) as file:
            while True:
                chunk = file.read(65536)
                if not chunk:
                    break
                yield chunk

    return StreamingResponse(file_iterator(), media_type="application/octet-stream")


@app.get("/session/{unique_session_id}/meta/{file_name}")
def unique_session_meta(unique_session_id: str, file_name: str):
    def file_iterator():
        with open(
                os.path.join(f"./sessions/{unique_session_id}/", f"{file_name}.txt"), mode="rb"
        ) as file:
            while True:
                chunk = file.read(65536)
                if not chunk:
                    break
                yield chunk

    return StreamingResponse(file_iterator(), media_type="application/octet-stream")


@app.delete("/session/{unique_session_id}")
def delete_session(unique_session_id: str):
    """
    Delete current session and all associated files.

    :return: None
    """
    session_dir = os.path.join("./sessions/", f"{unique_session_id}")

    if os.path.exists(session_dir):
        shutil.rmtree(session_dir)
        XRayStorage['UniqueSessionId'] = None
    else:
        raise HTTPException(status_code=404, detail="Session not found")
