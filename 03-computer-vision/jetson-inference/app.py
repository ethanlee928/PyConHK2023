import av
import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer
from jetson_inference import detectNet
from jetson_utils import cudaFromNumpy, cudaToNumpy

DETECTOR = detectNet("ssd-mobilenet-v2", threshold=0.5)

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

webrtc_streamer(key="example", video_frame_callback=callback)
