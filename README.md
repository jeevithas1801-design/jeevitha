🔬 AI Smart Microscope Assistant

A Web-Based Scientific Image Processing and Analysis Platform

📌 About the Project

The AI Smart Microscope Assistant is a web-based application developed using Python and Streamlit. It helps users upload, process and examine microscopic images using computer vision techniques.

The application provides image enhancement, brightness and contrast adjustment, grayscale conversion, edge detection and experimental circular feature detection.

It aims to make basic microscopic image analysis easier through a simple and interactive scientific dashboard.

🎯 Objectives

- Develop a web-based microscope image analysis platform.
- Upload and display microscopic images.
- Improve image visibility using brightness and contrast adjustment.
- Perform grayscale conversion and edge detection.
- Detect circular image features experimentally.
- Display image analysis results.
- Generate downloadable analysis reports.

✨ Features

1. Image Upload – Upload JPG, JPEG and PNG images.
2. Image Enhancement – Adjust brightness and contrast.
3. Grayscale Conversion – Convert images into grayscale.
4. Edge Detection – Identify image boundaries using Canny edge detection.
5. Circular Feature Detection – Detect circular candidates using the Hough Circle Transform.
6. Scientific Dashboard – Display image details and analysis results.
7. Histogram Analysis – Visualize pixel intensity distribution.
8. CSV Report – Download analysis information.
9. PDF Report – Generate downloadable scientific reports.

🛠️ Technologies Used

Technology| Purpose
Python| Programming language
Streamlit| Web application framework
OpenCV| Image processing
NumPy| Numerical operations
Pillow| Image handling
ReportLab| PDF report generation

💻 System Requirements

- Windows, Linux or macOS
- Python 3.10 or newer
- Minimum 4 GB RAM recommended
- Internet connection for installation
- VS Code or another Python editor

⚙️ Installation

1. Clone the repository

git clone https://github.com/YOUR-USERNAME/AI-Smart-Microscope-Assistant.git

2. Open the project folder

cd AI-Smart-Microscope-Assistant

3. Install the dependencies

python -m pip install -r requirements.txt

4. Run the application

python -m streamlit run app.py

5. Open the application

Streamlit will provide a local browser address, usually:

http://localhost:8501

🔬 Working Principle

1. Upload a microscopic image.
2. Adjust brightness and contrast.
3. Convert the image into grayscale.
4. Apply Canny edge detection.
5. Detect circular image features.
6. Display the analysis results.
7. Download the CSV or PDF report.

📁 Project Structure

AI-Smart-Microscope-Assistant/
│
├── app.py
├── requirements.txt
├── README.md
└── app_backup.py

🚀 Future Enhancements

- Machine learning-based cell detection.
- Deep learning image classification.
- Advanced image segmentation.
- Validated cell-type identification.
- Integration with digital microscopes.
- Cloud-based image analysis.
- Advanced scientific reporting.

⚠️ Limitations

The current circular feature detection uses traditional computer vision techniques. Detected circular candidates are not confirmed biological cells. Results are experimental and are not intended for medical diagnosis.

👩‍🔬 Project Information

Project Name: AI Smart Microscope Assistant

Domain: Biomedical Engineering and Artificial Intelligence

Platform: Python and Streamlit

Project Status: Working Prototype

---

Developed as an educational project to explore the application of computer vision in microscopic image analysis.