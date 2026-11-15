import streamlit as st
from PIL import Image, ImageOps
import cv2
import numpy as np
import io
import csv

st.set_page_config(page_title="AI Smart Microscope Assistant", page_icon="🔬🧬", layout="wide")

st.title("🔬🧬 AI Smart microscope Assistant")

st.subheader("welcome to our AI-powered scientific laboratory")

st.write("Upload microscopic images and explore intelligent image analysis")

st.divider()

st.header("Scientific Dashboard")

uploaded_file = st.file_uploader("Upload a micrescope image", type=["jpg", "jpeg", "png"])


if uploaded_file is not None:
    image=Image.open(uploaded_file).convert("RGB")
    image_array = np.array(image)
    st.header("Microscope Image Analysis")
    
    col1, col2 = st.columns(2)

    with col1:
        brightness = st.slider("Adjust Brightness", -100, 100, 0)

    with col2:
        contrast = st.slider("Adjust Contrast", 0.5, 3.0, 1.0, 0.1)

    enhanced = cv2.convertScaleAbs(image_array, alpha=contrast, beta=brightness)
    gray = cv2.cvtColor(enhanced, cv2.COLOR_RGB2GRAY)
    edges=cv2.Canny(gray, 50, 150)

    st.header("Cell Detection Settings")

    min_radius=st.slider("Minimum cell radius", 5, 40, 8)

    max_radius=st.slider("Maximum cell radius", min_radius + 1, 100, max(40, min_radius + 1))

    min_distance = st.slider("Minimum distance between cells", 10, 100, 20)

    sensitivity = st.slider("Detection sensitivity", 10, 80, 30)

    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=min_distance, param1=100, param2=sensitivity, minRadius=min_radius, maxRadius=max_radius)
    
    detected_image = enhanced.copy()

    if circles is not None:
        circles = np.round(circles[0]).astype(int)
        for x, y, radius in circles:
            cv2.circle(detected_image, (x,y), radius, (255, 0, 0), 2)
            cv2.circle(detected_image, (x,y), 2, (0, 255, 0), -1)
        object_count = len(circles)
    
    else:
        object_count = 0

    st.divider()
    st.header("Analysis Results")

    m1, m2, m3 = st.columns(3)

    m1.metric("Images Uploaded", 1)
    m2.metric("Objects Detected", object_count)
    m3.metric("System Status", "Ready")

    st.divider()
    st.header("Microscope images Viewer")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("Original Image")
        st.image(image_array, use_container_width=True)

    with c2:
        st.subheader("Enhanced Image")
        st.image(enhanced, use_container_width=True)

    with c3:
        st.subheader("Edge Detection")
        st.image(detected_image, use_container_width=True)

    st.divider()

    st.subheader("Edge Detection")
    st.image(edges, caption="OpenCV Edge Detection")
    st.success("Image processing completed!")
    
    st.write("###Detection Summary")
    st.write(f"Total cell-like objectes detected: {object_count}")
    st.write(f"Image dimensions: {image.width} x {image.height}")

    st.info("Detection is based on circular image features."
    "results are experimental and are not medical diagnoses.")

    report = io.StringIO()
    writer = csv.writer(report)

    writer.writerow(["AI Smart Microscope Analusis Report"])
    writer.writerow(["Image", uploaded_file.name])
    writer.writerow(["Image Width", image.width])
    writer.writerow(["Image Height", image.height])
    writer.writerow(["Object Detected", object_count])
    writer.writerow(["Brightness", brightness])
    writer.writerow(["Contrast", contrast])
    writer.writerow(["Detection Sensitivity", sensitivity])

    st.download_button(label="Download Analysis Report", data=report.getvalue(), file_name="microscope_analysis.csv", mime="text/csv")

else:
    st.info("Please upload  microscope image to begin analysis.")
    st.metric("Images Uploaded", 0)
    st.metric("Objects Detected", 0)
    st.write("System status: Waiting for image upload")

