"""

"""
import os
import cv2
import supervision as sv
from ultralytics import YOLO


class BoneSegmentation:
    """

    """
    def __init__(self):
        """
        Initializes an instance of the CreateDataset class.

        :return: None
        """
        self.images_directory = os.path.join(
            os.getcwd(), "boneage-training-dataset/boneage-training-dataset"
        )
        self.predicted_images_directory = os.path.join(os.getcwd(), "predictions")
        self.model = YOLO(
            "/home/filip/PycharmProjects/X-ray/runs/segment/yolo_custom/weights/best.pt"
        )

    def predict(self, image):
        """
        Apply object segmentation on an input image using a given model and annotate detected objects.

        :param image: The input image on which to perform object segmentation and annotation.
        :return: An annotated image with objects highlighted.
        """
        image = cv2.imread(image)
        mask_annotator = sv.MaskAnnotator()
        result = self.model(image, verbose=False)[0]
        detections = sv.Detections.from_ultralytics(result)
        annotated_image = mask_annotator.annotate(
            image.copy(), detections=detections
        )

        return annotated_image

    def multiple_prediction(self):
        pass
    