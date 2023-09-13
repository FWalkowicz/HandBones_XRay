import os
import numpy as np
import supervision as sv
from ultralytics import YOLO
import cv2
import secrets
from scipy.spatial.distance import cdist


def read_file(filename, token, name):
    try:
        with open(f"metadata/{filename}", "r") as file:
            lines = file.readlines()

        with open(f"./sessions/{token}/{name}.txt", "w") as new_file:
            for line in lines:
                new_file.write(line)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def draw_bbox_contours(image, all_contours, min_size: int, max_size: int):
    for contour in all_contours:
        if min_size < cv2.contourArea(contour) <= max_size:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)


def find_objects_contours(image, threshold_value, kernel_size):
    _, thresh = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    thresholded = cv2.morphologyEx(
        thresh, cv2.MORPH_CLOSE, np.ones((kernel_size, kernel_size), np.uint8)
    )
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


def find_center_bbox(detections, class_id: int) -> list:
    dots = []
    for dot in detections.xyxy[detections.class_id == class_id]:
        pt1 = (int((dot[0] + dot[2]) / 2), int((dot[1] + dot[3]) / 2))
        dots.append(pt1)
    return dots


def find_nearest_point(pt1, points):
    pt2 = points[cdist([pt1], points).argmin()]
    return pt2


def sort_by_x(point):
    return point[0]


def draw_phantom(image, points, neighbour_points) -> None:
    for point in points:
        pt2 = find_nearest_point(point, neighbour_points)
        cv2.line(image, pt1=point, pt2=pt2, color=(255, 255, 255), thickness=3)
        cv2.circle(image, point, 5, (255, 0, 0), cv2.FILLED)
        cv2.putText(
            image,
            f"{points.index(point)}",
            point,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 0, 0),
            1,
            cv2.LINE_AA,
        )


def phantom(image, detections):
    classes = [
        "Carpals",
        "Distal phalanges",
        "Intermediate phalanges",
        "Metacarpals",
        "Proximal phalanges",
        "Radius",
        "Ulna",
    ]
    points_0 = find_center_bbox(detections, 0)
    points_1 = find_center_bbox(detections, 1)
    points_2 = find_center_bbox(detections, 2)
    points_3 = find_center_bbox(detections, 3)
    points_4 = find_center_bbox(detections, 4)

    points_0 = sorted(points_0, key=sort_by_x)
    points_1 = sorted(points_1, key=sort_by_x)
    points_2 = sorted(points_2, key=sort_by_x)
    points_3 = sorted(points_3, key=sort_by_x)
    points_4 = sorted(points_4, key=sort_by_x)

    draw_phantom(image, points_1, points_2 + points_4)
    draw_phantom(image, points_2, points_4)
    draw_phantom(image, points_4, points_3)
    draw_phantom(image, points_3, points_0)

    for point in points_0:
        cv2.circle(image, point, 5, (255, 0, 0), cv2.FILLED)
        cv2.putText(
            image,
            f"{points_0.index(point)}",
            point,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 0, 0),
            1,
            cv2.LINE_AA,
        )

    for point in points_0:
        points_0.remove(point)
        pt2 = find_nearest_point(point, points_0)
        cv2.line(image, pt1=point, pt2=pt2, color=(255, 255, 255), thickness=3)
        points_0.append(point)

    points = {}
    for class_id, class_name in enumerate(classes):
        points[class_name] = find_center_bbox(detections, class_id)
        points[class_name] = sorted(points[class_name], key=sort_by_x)

    finger_bones_number = {
        "Carpals": 8,
        "Distal phalanges": 5,
        "Intermediate phalanges": 4,
        "Proximal phalanges": 5,
        "Metacarpals": 5,
    }
    finger_counts = {
        "Carpals": len(points["Carpals"]),
        "Distal phalanges": len(points["Distal phalanges"]),
        "Intermediate phalanges": len(points["Intermediate phalanges"]),
        "Proximal phalanges": len(points["Proximal phalanges"]),
        "Metacarpals": len(points["Metacarpals"]),
    }

    missing_bones = []

    for class_name, count in finger_counts.items():
        if count > 0:
            missing_bones.append(
                f"<p>Detected {count} {class_name}, missing {finger_bones_number[class_name] - count}</p>"
            )

    return image, missing_bones


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
        phantom_image, missing_bones = phantom(annotated_image.copy(), detections)

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
        gray_image = cv2.cvtColor(
            placeholder, cv2.COLOR_BGR2GRAY
        )  # Convert to grayscale
        _, bones_binary = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY)
        bones_contour, _ = cv2.findContours(
            bones_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
        )

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
            os.mkdir(f"./sessions/{self.token}")
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
        self.save_image("phantom", phantom_image)
        self.create_image_description("phantom")

        return self.token

    def save_image(self, name, image):
        cv2.imwrite(f"./sessions/{self.token}/{name}.jpg", image)

    def create_image_description(self, name):
        lorem = "Suspendisse faucibus, nisi id ullamcorper ultrices, nunc erat imperdiet ipsum, quis convallis augue orci sit amet diam. Curabitur iaculis turpis leo, lacinia congue libero mollis vitae. Mauris sit amet diam in orci aliquet tempor. In et pharetra sapien. Maecenas porta porttitor quam a maximus. Duis vitae erat ante. Nulla suscipit nibh eu nulla ullamcorper, a tristique mauris varius. Fusce suscipit feugiat ipsum, id malesuada leo pellentesque ut. Donec ut scelerisque sem. Cras pharetra finibus porttitor. "
        for dir_path, dir_names, file_names in os.walk(f"metadata"):
            for file_name in file_names:
                if self.filename.startswith(file_name[:-4]):
                    print(f"found {self.filename} ---- {file_name}")
                    read_file(file_name, self.token, name)
                    return
                else:
                    with open(f"./sessions/{self.token}/{name}.txt", "w") as f:
                        f.write(lorem)
                        f.close()
