import streamlit as st
import os
from io import BytesIO
import base64

# Function to display video
def show_video(video_path):
    st.video(video_path, format="video/mp4")

# Function to generate the "+" button
def render_upload_button():
    st.markdown("""
        <style>
        .upload-button {
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 1000;
            background-color: #1dbf73;
            color: white;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 2rem;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
        }
        .upload-button:hover {
            background: #17a567;
        }
        </style>
        <div class="upload-button" onclick="document.getElementById('file_input').click()">+</div>
        <input type="file" id="file_input" accept="video/*" style="display:none;" onchange="handleFileUpload(event)">
    """, unsafe_allow_html=True)

# Function to handle video upload and display
def handle_file_upload():
    uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])
    if uploaded_file is not None:
        # Save uploaded video to the Streamlit app directory
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Display the video after upload
        show_video(file_path)
        st.success(f"Video {uploaded_file.name} uploaded successfully!")

# Main Streamlit page layout
def main():
    # Create a directory to store uploaded videos if it doesn't exist
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    # Display upload button
    render_upload_button()

    # Handle file upload and display
    handle_file_upload()

if __name__ == "__main__":
    main()
