import os
from scipy.spatial.distance import cdist
import numpy as np
import supervision as sv
from ultralytics import YOLO
import cv2


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


def model_prediction(image, classes):
    model = YOLO(os.path.join(os.getcwd(), "models/all_bones.pt"))
    mask_annotator = sv.MaskAnnotator()
    result = model(image, verbose=False)[0]
    detections = sv.Detections.from_ultralytics(result)
    detections = detections[np.isin(detections.class_id, [0, 1, 2,3,4])]
    detections = detections[detections.confidence >= 0.70]
    annotated_image = mask_annotator.annotate(image, detections=detections)

    return annotated_image, detections


model = YOLO(os.path.join(os.getcwd(), "C:/Users/Filip/PycharmProjects/XRay/app/models/all_bones.pt"))
image = cv2.imread("C:/Users/Filip/PycharmProjects/XRay/images/broken.png")
"""
(h, w) = image.shape[:2]
(cX, cY) = (w // 2, h // 2)
M = cv2.getRotationMatrix2D((cX, cY), 45, 1.0)
image = cv2.warpAffine(image, M, (w, h))
"""

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
        cv2.putText(image, f"{points.index(point)}", point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

def phantom(image, detections, classes):

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

    draw_phantom(image, points_1, points_2+points_4)
    draw_phantom(image, points_2, points_4)
    draw_phantom(image, points_4, points_3)
    draw_phantom(image, points_3, points_0)

    for point in points_0:
        cv2.circle(image, point, 5, (255, 0, 0), cv2.FILLED)
        cv2.putText(image, f"{points_0.index(point)}", point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

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
            missing_bones.append(f"<p>Detected {count} {class_name}, missing {finger_bones_number[class_name] - count}</p>")

    return image, missing_bones

def start(image):
    classes = [
        "Carpals",
        "Distal phalanges",
        "Intermediate phalanges",
        "Metacarpals",
        "Proximal phalanges",
        "Radius",
        "Ulna",
    ]
    classe = []
    image = cv2.resize(image, (600, 600))

    # predykcja modelu
    annotated_image, detections = model_prediction(image, classe)
    polygons = [sv.mask_to_polygons(m) for m in detections.mask]
    box_annotator = sv.BoxAnnotator()
    labels = [
        f"{class_id, classes[class_id]} {confidence:0.2f}"
        for _, _, confidence, class_id, _ in detections
    ]
    phantom_image, missing_bones = phantom(annotated_image.copy(), detections, classes)
    annotated_frame = box_annotator.annotate(
        scene=image.copy(), detections=detections, labels=labels
    )

    Hori = np.concatenate((annotated_image, annotated_frame, phantom_image), axis=1)
    while True:
        cv2.imshow("Slider", Hori)
        if cv2.waitKey(1) == ord("q"):
            break



start(image)
