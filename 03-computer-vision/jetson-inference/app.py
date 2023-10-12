import av
import cv2
from jtop import jtop
import streamlit as st
from streamlit_webrtc import webrtc_streamer
from jetson_inference import detectNet
from jetson_utils import cudaFromNumpy, cudaToNumpy


# Using pre-trained mobilenet-v2 from downloaded models
@st.cache_resource
def load_model():
    return detectNet("ssd-mobilenet-v2", threshold=0.5)


DETECTOR = load_model()


def get_jetson_stats():
    with jtop() as jetson:
        if jetson.ok():
            return jetson.stats


def detect(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    cuda_img = cudaFromNumpy(img)
    detections = DETECTOR.Detect(cuda_img, overlay="box,labels,conf")
    np_img = cudaToNumpy(cuda_img)
    np_img = cv2.cvtColor(np_img, cv2.COLOR_RGBA2BGR)
    return np_img


def callback(frame):
    img = frame.to_ndarray(format="bgr24")
    img = detect(img)
    return av.VideoFrame.from_ndarray(img, format="bgr24")


ctx = webrtc_streamer(
    key="object-detection",
    video_frame_callback=callback,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

gpu_bar = st.progress(0, text=f"GPU Usage(%): :green[0]")
while ctx.state.playing:
    gpu_usage = 0
    color = "green"
    if jetson_stats := get_jetson_stats():
        gpu_usage = int(jetson_stats.get("GPU", 0))
        if 0 <= gpu_usage < 50:
            color = "green"
        elif 50 <= gpu_usage < 90:
            color = "orange"
        else:
            color = "red"
    gpu_bar.progress(gpu_usage, text=f"GPU Usage(%): :{color}[{gpu_usage}]")
