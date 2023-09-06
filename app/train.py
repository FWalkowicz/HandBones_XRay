import os
import numpy as np
import supervision as sv
from ultralytics import YOLO
import cv2
import secrets


def draw_bbox_contours(image, all_contours, min_size: int, max_size: int):
    for contour in all_contours:
        if min_size < cv2.contourArea(contour) <= max_size:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)


def find_objects_contours(image, threshold_value, kernel_size):
    _, thresh = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    thresholded = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, np.ones((kernel_size, kernel_size), np.uint8))
    contours_white, hierarchy_white = cv2.findContours(
        image=thresholded, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_NONE
    )

    return contours_white


def model_prediction(image):
    model = YOLO(os.path.join(os.getcwd(), "models/all_bones.pt"))
    mask_annotator = sv.MaskAnnotator()
    result = model(image, verbose=False)[0]
    detections = sv.Detections.from_ultralytics(result)
    # detections = detections[detections.class_id == 0]
    detections = detections[detections.confidence >= 0.70]
    annotated_image = mask_annotator.annotate(image, detections=detections)

    return annotated_image, detections


class XRayPredictions:
    def __init__(self, image, filename):
        self.model = YOLO(os.path.join(os.getcwd(), "models/all_bones.pt"))
        self.image = image
        self.token = secrets.token_urlsafe(2)
        self.filename = filename

    def start(self):
        image = cv2.resize(self.image, (600, 600))

        # predykcja modelu
        annotated_image, detections = model_prediction(image)
        polygons = [sv.mask_to_polygons(m) for m in detections.mask]

        # Wyszukanie metalowych obiektów w pierwotnym zdjęciu
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        contours_white = find_objects_contours(image_gray, 235, 5)

        # puste zdjęcie, na które będzie nałożona maska
        img = np.zeros((600, 600), dtype=np.uint8)  # Use a grayscale image for the mask

        # rysowanie predykcji modelu
        for i in range(len(detections.confidence)):
            cv2.drawContours(img, polygons[i], -1, (255, 255, 255), cv2.FILLED)

        # maska z samymi kośćmi zktóre usunie się z odwróconego zdjęcia
        inverted_mask = cv2.bitwise_not(img)

        # Same kości
        placeholder = cv2.bitwise_not(image, mask=img)
        gray_image = cv2.cvtColor(placeholder, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        _, bones_binary = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY)
        bones_contour, _ = cv2.findContours(bones_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        # Usunięcie kości ze zdjęcia
        inverted_image = cv2.bitwise_not(image, mask=inverted_mask)
        inverted_image[inverted_mask == 0] = 255
        inverted_image_gray = cv2.cvtColor(inverted_image, cv2.COLOR_BGR2GRAY)
        inverted_image_gray = inverted_image_gray[0:390, 0:600]
        contours = find_objects_contours(inverted_image_gray, 140, 3)

        # metalowe obiekty
        draw_bbox_contours(image, contours_white, 200, 10000)

        # zaznaczanie wszystkich zmian poza kośćmi
        draw_bbox_contours(image, contours, 200, 10000)
        try:
            os.mkdir(f'./sessions/{self.token}')
        except OSError as error:
            print(error)
        self.save_image("prediction", image)
        self.create_image_description("prediction")
        self.save_image("model_prediction", annotated_image)
        self.create_image_description("model_prediction")
        self.save_image("without_bones", inverted_image)
        self.create_image_description("without_bones")
        self.save_image("only_bones", placeholder)
        self.create_image_description("only_bones")

        return self.token

    def save_image(self, name, image):
        cv2.imwrite(f"./sessions/{self.token}/{name}.jpg", image)

    def create_image_description(self, name):
        lorem = "Suspendisse faucibus, nisi id ullamcorper ultrices, nunc erat imperdiet ipsum, quis convallis augue orci sit amet diam. Curabitur iaculis turpis leo, lacinia congue libero mollis vitae. Mauris sit amet diam in orci aliquet tempor. In et pharetra sapien. Maecenas porta porttitor quam a maximus. Duis vitae erat ante. Nulla suscipit nibh eu nulla ullamcorper, a tristique mauris varius. Fusce suscipit feugiat ipsum, id malesuada leo pellentesque ut. Donec ut scelerisque sem. Cras pharetra finibus porttitor. "
        for dir_path, dir_names, file_names in os.walk(f"./metadata"):
            for dir_name in dir_names:
                if dir_name == self.filename:
                    pass
                else:
                    with open(f'./sessions/{self.token}/{name}.txt', 'w') as f:
                        f.write(lorem)
                        f.close()

