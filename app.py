import streamlit as st
import os
import shutil

# Create an "uploads" folder to store videos if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Title of the web app
st.title("Video Streaming and Uploading Website")

# File uploader for video files
uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])

# Save the uploaded file to the "uploads" folder
if uploaded_file is not None:
    file_path = os.path.join("uploads", uploaded_file.name)
    
    # Save the uploaded video to the folder
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
    
    # Display video on the webpage
    st.video(file_path)

# Display list of already uploaded videos
st.subheader("Uploaded Videos")
uploaded_videos = os.listdir("uploads")

if len(uploaded_videos) > 0:
    for video in uploaded_videos:
        video_path = os.path.join("uploads", video)
        st.write(video)
        st.video(video_path)
else:
    st.write("No videos uploaded yet.")
