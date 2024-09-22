import streamlit as st
import os

# Create an "uploads" folder to store videos if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Title of the web app
st.title("Video Streaming and Uploading Website")

# File uploader for video files
uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])

# Check if the uploaded file is not None
if uploaded_file is not None:
    file_path = os.path.join("uploads", uploaded_file.name)
    
    # Check if the file already exists
    if os.path.exists(file_path):
        st.warning(f"File '{uploaded_file.name}' already exists. Please upload a different file.")
    else:
        # Save the uploaded video to the folder
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        
        # Display the newly uploaded video
        st.video(file_path)

# Display list of already uploaded videos
st.subheader("Select and Play an Uploaded Video")
uploaded_videos = os.listdir("uploads")

if len(uploaded_videos) > 0:
    # Create a dropdown or radio button to allow selecting a video to play
    selected_video = st.selectbox("Choose a video to play:", uploaded_videos)

    if selected_video:
        video_path = os.path.join("uploads", selected_video)
        st.video(video_path)
else:
    st.write("No videos uploaded yet.")
