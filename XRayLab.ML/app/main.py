from fastapi import FastAPI, UploadFile, HTTPException, Depends, status
from fastapi.responses import StreamingResponse
import shutil
from train import XRayPredictions
import cv2
import os
from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import base64


app = FastAPI()
security = HTTPBasic()

XRayStorage = {"UniqueSessionId": None, "Files": []}
UserStorage = {
    "clientId": "comcore",
    "clientSecret": "75TF3R7HrqFB"
}


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"comcore"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"75TF3R7HrqFB"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/auth")
def read_current_user(credentials: Annotated[str, Depends(get_current_username)]):
    return {"username": credentials}


@app.post("/executeAI")
async def execute_ai(input_image: UploadFile):
    """
    Execute AI processing on an uploaded X-ray image.

    :param input_image: The X-ray image file to be processed (JPEG or PNG).
    :return: Information about the processed session
    """
    if not input_image.filename.lower().endswith((".jpg", ".jpeg", ".png")):
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
    XRayStorage["UniqueSessionId"] = token
    result = []

    for dir_path, _, file_names in os.walk(
        f"./sessions/{XRayStorage['UniqueSessionId']}"
    ):
        for file_name in file_names:
            if file_name.endswith(".jpg"):
                file_dict = {"FileName": file_name, "Type": "Image"}
            if file_name.endswith(".txt"):
                file_dict = {"FileName": file_name, "Type": "Metadata"}

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
            session_dict = {"UniqueSessionId": os.path.basename(dir_path), "Files": []}

            for file_name in file_names:
                if file_name.endswith(".jpg"):
                    file_dict = {"FileName": file_name, "Type": "Image"}

                if file_name.endswith(".txt"):
                    file_dict = {"FileName": file_name, "Type": "Metadata"}

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
                file_dict = {"FileName": file_name, "Type": "Image"}

            if file_name.endswith(".txt"):
                file_dict = {"FileName": file_name, "Type": "Metadata"}

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
            os.path.join(f"./sessions/{unique_session_id}/", f"{file_name}.jpg"),
            mode="rb",
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
            os.path.join(f"./sessions/{unique_session_id}/", f"{file_name}.txt"),
            mode="rb",
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
        XRayStorage["UniqueSessionId"] = None
    else:
        raise HTTPException(status_code=404, detail="Session not found")


@app.delete("/sessions")
def delete_sessions():
    """
    Delete all sessions and all associated files.

   :return: None
   """
    session_dir = os.path.join("./sessions/")
    for _, dir_names, _ in os.walk(session_dir):
        for dir_name in dir_names:
            shutil.rmtree(os.path.join(session_dir, dir_name))
