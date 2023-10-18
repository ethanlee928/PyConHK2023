import av
import cv2
from jtop import jtop
import streamlit as st
from streamlit_webrtc import webrtc_streamer
from jetson_inference import detectNet
from jetson_utils import cudaFromNumpy, cudaToNumpy, videoSource, videoOutput


@st.cache_resource
def load_model():
    return detectNet("ssd-mobilenet-v2", threshold=0.5)


@st.cache_resource
def load_videoSource():
    return videoSource("v4l2:///dev/video0")


SOURCE = load_videoSource()
DETECTOR = load_model()


st.title("Object Detection with SSD MobilenetV2 👀")
with st.empty():
    while True:
        img = SOURCE.Capture(timeout=1000)
        if img is None:
            continue
        detections = DETECTOR.Detect(img, overlay="box,labels,conf")
        np_img = cudaToNumpy(img, cv2.COLOR_RGBA2BGR)
        st.image(np_img, caption="Detection Results")
