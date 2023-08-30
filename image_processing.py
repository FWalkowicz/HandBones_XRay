"""

"""
import os
import cv2
import supervision as sv
from ultralytics import YOLO


class CreateDataset:
    """
    A class for creating and managing datasets of images.
    This class provides methods to start the dataset creation process,
    read images, and save images to the dataset.

    """

    def __int__(self, number_of_images):
        """
        Initializes an instance of the CreateDataset class.

        :param number_of_images: number of images to convert
        :return: None
        """
        self.number_of_images = number_of_images
        self.images_directory = os.path.join(
            os.getcwd(), "boneage-training-dataset/boneage-training-dataset"
        )
        self.predicted_images_directory = os.path.join(os.getcwd(), "predictions")
        self.model = YOLO(
            "/home/filip/PycharmProjects/X-ray/runs/segment/yolo_custom/weights/best.pt"
        )

    def start(self):
        """
        Initiates the dataset creation process.

        :return:
        """
        pass

    @staticmethod
    def read_image(image_id):
        """
        Reads an image from a source.
        This method is used to read an image from source and process it for the dataset.

        :return:
        """
        image = cv2.imread(image_id)

        return image

    @staticmethod
    def save_image(image, number):
        """
        Saves an image to the dataset.
        This method saves a previously read image to the dataset.

        :return: None
        """
        cv2.imwrite(f"prediction{number}", image)

    def predict(self, image):
        """
        Apply object segmentation on an input image using a given model and annotate detected objects.

        :param image: The input image on which to perform object segmentation and annotation.
        :return: An annotated image with objects highlighted.
        """
        mask_annotator = sv.MaskAnnotator()
        result = self.model(image, verbose=False)[0]
        detections = sv.Detections.from_ultralytics(result)
        annotated_image = mask_annotator.annotate(
            image.copy(), detections=detections[0]
        )

        return annotated_image
