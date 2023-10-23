# Streamlit &mdash; Creating Interactive Websites with Ease

Materials for PyCon Hong Kong 2023

## 1. Abstract

Streamlit is a Python library for creating interactive web applications with ease. It provides built-in tools and widgets for adding interactivity, integrates with popular data science libraries like pandas and scikit-learn, and allows for the deployment of web apps with just a few lines of code.

This talk will explore the different potentials of using Streamlit with three examples: creating a static page, a page for data visualization, and a page for real-time computer vision applications. First, we will discuss the basics of Streamlit by building a static page, which is suitable even for Python beginners. It aims to illustrate the convenience of Streamlit by showing how one can create a styled, responsive self-introduction page in minutes.
For data visualization, we will create an interactive page of Monte-Carlo Simulation on the stock market, which aims to illustrate the integration between Streamlit and some popular data science libraries.

Lastly, we will utilize the open-source library streamlit-webrtc, which allows users to easily use real-time video/audio streams on Streamlit apps, to build a real-time computer vision application.

In short, this talk introduces an emerging Python library—Streamlit. It is a powerful tool for data scientists and machine learning engineers for research and development.

## 2. How to Start

**Remarks:**

- The following instructions are only for `01-intro-page`, `02-simulation` and `03-computer-vision/haarcascade` example.
- `03-computer-vision/jetson-inference` requires a Jetson Nano to run.

### 2.0 Install the dependecies using virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

### 2.1 Start 01-intro-page

```bash
cd 01-intro-page
streamlit run app.py
```

### 2.2 Start 02-simulation

```bash
cd 02-simulation
streamlit run app.py
```

### 2.3 Start haarcascade example

```bash
cd 03-computer-vision/haarcascade
streamlit run app.py
```

## 3. Streamlit with Jetson-Inference

### 3.0 Prerequisite

| **Device**       | Jetson Nano |
| ---------------- | ----------- |
| **JetPack Ver.** | 4.6         |
| **Camera**       | USB Camera  |

#### Docker Environment

This example has to be run inside a Docker environment.

##### Build the Docker image

```bash
cd 03-computer-vision/jetson-inference/
docker build -t streamlit-jetson-inference .
```

##### Start the Docker container

```bash
cd 03-computer-vision/jetson-inference/
./start.sh
```

### 3.1 Start examples

**prerequisite**: Inside the docker container

#### Download the models
```bash
cd /jetson-inference/tools
./download-models.sh    # Select the models you want to download
```

```bash
cd 03-computer-vision/jetson-inference

# webrtc example
streamlit run webrtc.py

# v4l2 example
streamlit run v4l2.py
```
