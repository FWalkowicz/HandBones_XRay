from pprint import pprint
import os
from image_processing import BoneSegmentation
import numpy as np
import pandas
import supervision as sv
from roboflow import Roboflow
from ultralytics import YOLO
import cv2
"""
rf = Roboflow(api_key="iT6ldD45bmnaYpuFrf8B")
project = rf.workspace("yolo-qdpfg").project("bonesss")
dataset = project.version(2).download("yolov8")


model = YOLO("./models/yolov8m-seg.pt")
result = model.train(
    data="/home/filip/PycharmProjects/X-ray/bonesss-2/data.yaml",
    imgsz=640,
    epochs=10,
    batch=8,
    name="yolo_custom",
)

elements = []
model = YOLO('/home/filip/PycharmProjects/X-ray/runs/segment/yolo_custom/weights/best.pt')
image_dir = '/home/filip/PycharmProjects/X-ray/boneage-training-dataset/boneage-training-dataset'
img_list = os.listdir(image_dir)
for i in range(50):
    image = cv2.imread(os.path.join(image_dir, img_list[i]))
    mask_annotator = sv.MaskAnnotator()
    result = model(image, verbose=False)[0]
    detections = sv.Detections.from_ultralytics(result)
    detections_filtered = detections[detections.confidence > 0.75]

#    for i in range(len(detections.confidence)):
#        elements.append([i, detections.mask[i]])

    elements_list = pandas.DataFrame(data=elements)
    pprint(elements_list)
    annotated_image = mask_annotator.annotate(image.copy(), detections=detections[0])
    #sv.plot_image(image=annotated_image, size=(8, 8))
    cv2.imwrite(f'predictions/pred{i}.jpg', annotated_image)
    print(f'image number {i} saved!')

"""
model = YOLO('/home/filip/PycharmProjects/X-ray/runs/segment/yolo_custom/weights/best.pt')
image = cv2.imread('hand_no_good_hand_bad.png')
image = cv2.resize(image, (600, 600))
mask_annotator = sv.MaskAnnotator()
result = model(image, verbose=False)[0]
detections = sv.Detections.from_ultralytics(result)
annotated_image = mask_annotator.annotate(image, detections=detections[0])
#sv.plot_image(image=annotated_image, size=(8, 8))
polygons = [sv.mask_to_polygons(m) for m in detections.mask]


img = np.zeros((600, 600, 3), dtype=np.uint8)
for i in range(len(detections.confidence)):
    cv2.drawContours(img, polygons[i], -1, (i*5, i*10, 255-i*20), 2)

bone = BoneSegmentation
predict = bone.predict(image=image)

while True:
    cv2.imshow('img', img)
    cv2.imshow('bone', predict)
    if cv2.waitKey(1) == ord('q'):
        break
