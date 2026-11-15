import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import csv
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Smart Microscope Assistant",
    page_icon="🔬",
    layout="wide"
)


# --------------------------------------------------
# 2. PROFESSIONAL DESIGN
# --------------------------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #0b1220;
    color: #e5edf7;
}

[data-testid="stSidebar"] {
    background-color: #111c2e;
    border-right: 1px solid #263750;
}

h1, h2, h3 {
    color: #eaf3ff;
}

p, label {
    color: #c6d3e3;
}

div[data-testid="stMetric"] {
    background-color: #14243a;
    border: 1px solid #263d5b;
    padding: 16px;
    border-radius: 12px;
}

[data-testid="stFileUploader"] {
    background-color: #14243a;
    border: 1px dashed #3c78ad;
    border-radius: 12px;
    padding: 12px;
}

div.stDownloadButton > button {
    background-color: #1677d2;
    color: white;
    border-radius: 8px;
    border: none;
}

hr {
    border-color: #263750;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 3. SIDEBAR AND NAVIGATION
# --------------------------------------------------

with st.sidebar:
    st.title("🔬 AI MICRO LAB")
    st.caption("Scientific Image Analysis Platform")

    st.divider()

    page = st.selectbox(
        "Navigation",
        [
            "Dashboard",
            "Image Analysis",
            "Detection Results",
            "Reports",
            "About Project"
        ]
    )

    st.divider()

    st.subheader("Upload Microscope Image")

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"]
    )

    st.divider()

    st.caption("Project Version: 2.0")
    st.caption("Python | Streamlit | OpenCV")


# --------------------------------------------------
# 4. MAIN HEADER
# --------------------------------------------------

st.title("🔬 AI Smart Microscope Assistant")

st.markdown(
    "### Scientific Image Processing and Analysis Platform"
)

st.write(
    "Upload microscopic images, enhance image quality "
    "and explore experimental computer vision analysis."
)

st.divider()


# --------------------------------------------------
# 5. IMAGE PROCESSING
# --------------------------------------------------

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")
    image_array = np.array(image)

    st.sidebar.subheader("Image Settings")

    brightness = st.sidebar.slider(
        "Brightness",
        -100, 100, 0
    )

    contrast = st.sidebar.slider(
        "Contrast",
        0.5, 3.0, 1.0, 0.1
    )

    st.sidebar.subheader("Detection Settings")

    min_radius = st.sidebar.slider(
        "Minimum radius",
        5, 40, 8
    )

    max_radius = st.sidebar.slider(
        "Maximum radius",
        min_radius + 1, 100,
        max(40, min_radius + 1)
    )

    min_distance = st.sidebar.slider(
        "Minimum distance",
        10, 100, 20
    )

    sensitivity = st.sidebar.slider(
        "Detection sensitivity",
        10, 80, 30
    )

    # Image enhancement
    enhanced = cv2.convertScaleAbs(
        image_array,
        alpha=contrast,
        beta=brightness
    )

    # Grayscale conversion
    gray = cv2.cvtColor(
        enhanced,
        cv2.COLOR_RGB2GRAY
    )

    # Edge detection
    edges = cv2.Canny(
        gray,
        50,
        150
    )

    # Circular feature detection
    blurred = cv2.GaussianBlur(
        gray,
        (9, 9),
        2
    )

    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=min_distance,
        param1=100,
        param2=sensitivity,
        minRadius=min_radius,
        maxRadius=max_radius
    )

    detected_image = enhanced.copy()

    if circles is not None:
        circles = np.round(
            circles[0]
        ).astype(int)

        for x, y, radius in circles:
            cv2.circle(
                detected_image,
                (x, y),
                radius,
                (255, 0, 0),
                2
            )

            cv2.circle(
                detected_image,
                (x, y),
                2,
                (0, 255, 0),
                -1
            )

        object_count = len(circles)

    else:
        object_count = 0

    # Histogram data
    histogram = cv2.calcHist(
        [gray],
        [0],
        None,
        [256],
        [0, 256]
    ).flatten()


    # --------------------------------------------------
    # 6. DASHBOARD PAGE
    # --------------------------------------------------

    if page == "Dashboard":

        st.header("📊 Scientific Dashboard")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Images Uploaded",
            "1"
        )

        c2.metric(
            "Circular Candidates",
            object_count
        )

        c3.metric(
            "System Status",
            "Ready"
        )

        st.divider()

        st.subheader("Current Image")

        col1, col2 = st.columns(2)

        with col1:
            st.image(
                image_array,
                caption="Original Microscope Image",
                use_container_width=True
            )

        with col2:
            st.image(
                detected_image,
                caption="Experimental Detection Output",
                use_container_width=True
            )

        st.info(
            "Upload an image using the sidebar to begin analysis."
        )


    # --------------------------------------------------
    # 7. IMAGE ANALYSIS PAGE
    # --------------------------------------------------

    elif page == "Image Analysis":

        st.header("🖼️ Image Analysis")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.image(
                image_array,
                caption="Original Image",
                use_container_width=True
            )

        with c2:
            st.image(
                enhanced,
                caption="Enhanced Image",
                use_container_width=True
            )

        with c3:
            st.image(
                gray,
                caption="Grayscale Image",
                use_container_width=True
            )

        st.divider()

        st.subheader("Edge Detection")

        st.image(
            edges,
            caption="Canny Edge Detection",
            use_container_width=True
        )

        st.success("Image processing completed!")


    # --------------------------------------------------
    # 8. DETECTION RESULTS PAGE
    # --------------------------------------------------

    elif page == "Detection Results":

        st.header("🧬 Detection Results")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Detected Candidates",
            object_count
        )

        c2.metric(
            "Image Width",
            image.width
        )

        c3.metric(
            "Image Height",
            image.height
        )

        st.divider()

        st.subheader("Detected Image")

        st.image(
            detected_image,
            caption="Experimental Circular Feature Detection",
            use_container_width=True
        )

        st.subheader("Pixel Intensity Histogram")

        st.bar_chart(histogram)

        st.info(
            "Detection identifies circular image features. "
            "It does not confirm cell identity or provide "
            "a medical diagnosis."
        )


    # --------------------------------------------------
    # 9. REPORTS PAGE
    # --------------------------------------------------

    elif page == "Reports":

        st.header("📁 Analysis Reports")

        st.write(
            "Download the analysis details for your uploaded image."
        )

        # CSV report
        csv_report = io.StringIO()

        writer = csv.writer(csv_report)

        writer.writerow([
            "AI Smart Microscope Analysis Report"
        ])

        writer.writerow([
            "Image Name",
            uploaded_file.name
        ])

        writer.writerow([
            "Image Width",
            image.width
        ])

        writer.writerow([
            "Image Height",
            image.height
        ])

        writer.writerow([
            "Circular Candidates",
            object_count
        ])

        writer.writerow([
            "Brightness",
            brightness
        ])

        writer.writerow([
            "Contrast",
            contrast
        ])

        writer.writerow([
            "Detection Sensitivity",
            sensitivity
        ])

        st.download_button(
            "⬇️ Download CSV Report",
            data=csv_report.getvalue(),
            file_name="microscope_analysis.csv",
            mime="text/csv"
        )

        # PDF report
        pdf_buffer = io.BytesIO()

        document = SimpleDocTemplate(
            pdf_buffer,
            pagesize=letter
        )

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "AI Smart Microscope Assistant",
                styles["Title"]
            )
        )

        story.append(Spacer(1, 15))

        story.append(
            Paragraph(
                "Scientific Image Analysis Report",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1, 15))

        report_data = [
            ["Parameter", "Result"],
            ["Image Name", escape(uploaded_file.name)],
            ["Image Width", str(image.width)],
            ["Image Height", str(image.height)],
            ["Circular Candidates", str(object_count)],
            ["Brightness", str(brightness)],
            ["Contrast", str(contrast)],
            ["Detection Sensitivity", str(sensitivity)]
        ]

        report_table = Table(
            report_data,
            colWidths=[220, 250]
        )

        report_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0),
                 colors.HexColor("#17365D")),
                ("TEXTCOLOR", (0, 0), (-1, 0),
                 colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5,
                 colors.grey),
                ("PADDING", (0, 0), (-1, -1), 9),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
            ])
        )

        story.append(report_table)

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "Note: Circular candidate detection is experimental "
                "and does not establish cell identity or provide "
                "a medical diagnosis.",
                styles["BodyText"]
            )
        )

        document.build(story)

        pdf_buffer.seek(0)

        st.download_button(
            "⬇️ Download PDF Report",
            data=pdf_buffer.getvalue(),
            file_name="microscope_analysis_report.pdf",
            mime="application/pdf"
        )


# --------------------------------------------------
# 10. ABOUT PROJECT PAGE
# --------------------------------------------------

    elif page == "About Project":

        st.header("🔬 About the Project")

        st.write(
            "The AI Smart Microscope Assistant is a web-based "
            "microscopic image processing application."
        )

        st.subheader("Technologies Used")

        st.markdown("""
        - Python
        - Streamlit
        - OpenCV
        - NumPy
        - Pillow
        - ReportLab
        """)

        st.subheader("Project Objectives")

        st.markdown("""
        - Microscopic image uploading
        - Image enhancement
        - Grayscale conversion
        - Edge detection
        - Experimental circular feature detection
        - Analysis report generation
        """)

        st.subheader("Future Development")

        st.write(
            "Machine learning, image segmentation, "
            "validated cell classification and cloud deployment."
        )


else:

    st.header("📊 Scientific Dashboard")

    st.info(
        "Please upload a microscope image using the sidebar "
        "to begin image analysis."
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Images Uploaded", 0)
    c2.metric("Detected Candidates", 0)
    c3.metric("System Status", "Waiting")