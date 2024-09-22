import streamlit as st
import os

# Create an "uploads" folder to store videos if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Sidebar for uploading videos
st.sidebar.title("Upload Your Video")
uploaded_file = st.sidebar.file_uploader("Choose a video file", type=["mp4", "avi", "mov", "mkv"])

# Save the uploaded file
if uploaded_file is not None:
    file_path = os.path.join("uploads", uploaded_file.name)
    
    # Check if the file already exists
    if os.path.exists(file_path):
        st.sidebar.warning(f"File '{uploaded_file.name}' already exists.")
    else:
        # Save the uploaded video to the folder
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.sidebar.success(f"File '{uploaded_file.name}' uploaded successfully!")

# Main title
st.title("YourTube: Video Streaming")

# Display search bar
search_query = st.text_input("Search for a video", "")

# Display list of uploaded videos
st.subheader("Uploaded Videos")
uploaded_videos = os.listdir("uploads")

if len(uploaded_videos) > 0:
    # Filter videos based on search query
    if search_query:
        filtered_videos = [v for v in uploaded_videos if search_query.lower() in v.lower()]
    else:
        filtered_videos = uploaded_videos

    # Show videos in grid layout
    num_columns = 3  # Number of videos per row
    video_chunks = [filtered_videos[i:i + num_columns] for i in range(0, len(filtered_videos), num_columns)]

    for chunk in video_chunks:
        cols = st.columns(num_columns)
        for i, video in enumerate(chunk):
            with cols[i]:
                st.image("https://via.placeholder.com/150", caption=video)  # Placeholder for thumbnail
                if st.button(f"Play {video}", key=video):
                    st.video(os.path.join("uploads", video))
else:
    st.write("No videos uploaded yet.")

