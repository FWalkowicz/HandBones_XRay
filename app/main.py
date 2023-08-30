import pandas
import streamlit as st
from ultralytics import YOLO
import supervision as sv
import cv2
from PIL import Image
from numpy import asarray

DEFAULT_IMAGE = "img3.jpg"
elements = []
elements_list = []

# Setting page layout
st.set_page_config(
    page_title="X-ray bone segmentation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("X-ray bone segmentation - choose your image and start processing!")
st.sidebar.header("ML Model Config")
column_left, column_right = st.columns(2)

with st.sidebar:
    add_selectbox = st.sidebar.selectbox(
        "Select image here:", ("Email", "Home phone", "Mobile phone")
    )
    add_radio = st.radio("Choose a shipping method", ("Image", "Webcam"))
    if add_radio == "Image":
        source_img = st.sidebar.file_uploader(
            "Choose an image...", type=("jpg", "jpeg", "png", "bmp", "webp")
        )
    confidence = float(st.sidebar.slider("Select Model Confidence", 25, 100, 40)) / 100
    selected_id = st.multiselect("choose id:", options=elements_list)
    print(elements_list, selected_id, elements)


with column_left:
    if source_img:
        st.image(Image.open(source_img), width=600)
    else:
        st.image(DEFAULT_IMAGE, width=600)

with column_right:
    if source_img:
        image = asarray(Image.open(source_img))

    else:
        image = cv2.imread(DEFAULT_IMAGE)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    model = YOLO(
        "/home/filip/PycharmProjects/X-ray/runs/segment/yolo_custom/weights/best.pt"
    )
    mask_annotator = sv.MaskAnnotator()
    result = model(image, verbose=False)[0]
    detections = sv.Detections.from_ultralytics(result)
    for i in range(len(detections.confidence)):
        elements.append(i)
    elements_list = pandas.DataFrame(data=elements)
    annotated_image = mask_annotator.annotate(image.copy(), detections=detections[selected_id])
    st.image(annotated_image, width=600)
    print(elements_list, selected_id, elements)
