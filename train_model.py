import os
from roboflow import Roboflow
from ultralytics import YOLO


class CreateCustomModel:
    """
    A class for creating and training custom YOLO object detection models using Roboflow and Ultralytics.

    """
    def __init__(self):
        self.current_path = os.path.join(os.getcwd(), 'app/models/')

    @staticmethod
    def download_dataset(api_key, workspace, project, version):
        """
        Download a specific version of a dataset from Roboflow using the given API key, workspace, and project information.

        :param api_key: Your Roboflow API key used for authentication.
        :param workspace: The name of the Roboflow workspace containing the target project.
        :param project: The name of the specific project within the workspace.
        :param version: Specific version of dataset to download.
        :return: None
        """
        rf = Roboflow(api_key=api_key)
        project = rf.workspace(workspace).project(project)
        project.version(version).download("yolov8")

    def train(self, model_name, yaml_path):
        """
        Train a YOLO model using the specified configuration.

        :param model_name: The name of the model used for training.
        :param yaml_path:
        :return: None
        """
        model = YOLO(f"{self.current_path}{model_name}.pt")
        model.train(
            data=yaml_path,
            imgsz=640,
            epochs=10,
            batch=8,
            name=f"{model_name}-custom",
        )

    def validate(self, model):
        pass

    def test(self):
        pass

