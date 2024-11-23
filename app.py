import streamlit as st
import cv2
import tempfile
import os

# Set the title and description
st.title("Video Uploader and Viewer")
st.write("Upload a video file and preview it below.")

# Video upload functionality
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov", "mkv"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_filepath = temp_file.name

    # Display the video player
    st.video(temp_filepath)

    # Extract video details using OpenCV
    cap = cv2.VideoCapture(temp_filepath)
    if cap.isOpened():
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = frame_count / fps
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        st.write(f"**Video Details:**")
        st.write(f"- Resolution: {width}x{height}")
        st.write(f"- Frame Count: {frame_count}")
        st.write(f"- FPS: {fps}")
        st.write(f"- Duration: {duration:.2f} seconds")
    else:
        st.error("Error reading the video file.")
    cap.release()

    # Option to download the uploaded file
    with open(temp_filepath, "rb") as file:
        st.download_button("Download Video", file, uploaded_file.name)

    # Clean up the temporary file after use
    os.remove(temp_filepath)
