import streamlit as st
from PIL import Image
import os
import json

# Create folders to store uploaded images and text metadata
if not os.path.exists('uploads'):
    os.makedirs('uploads')

if not os.path.exists('metadata'):
    os.makedirs('metadata')

# Streamlit title and description
st.set_page_config(page_title="Photo Gallery", layout="wide")
st.title("TEC SHORT")
st.write("Upload your photos and interact with them by liking or disliking!")

# Photo upload widget
st.sidebar.header("Upload Photo")
uploaded_file = st.sidebar.file_uploader("Choose a photo...", type=["jpg", "jpeg", "png"])

# Text input widget for description
description = st.sidebar.text_area("Enter a description for the photo")

# Button to submit the photo and text
if st.sidebar.button("Upload"):
    if uploaded_file is not None and description:
        # Save the image
        image_path = os.path.join("uploads", uploaded_file.name)
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Save the description, likes, dislikes as metadata
        metadata_path = os.path.join("metadata", uploaded_file.name + ".json")
        metadata = {
            "description": description,
            "likes": 0,
            "dislikes": 0
        }
        with open(metadata_path, "w") as f:
            json.dump(metadata, f)

        st.sidebar.success(f"Uploaded and saved: {uploaded_file.name} with description")
    else:
        st.sidebar.error("Please upload a photo and enter a description.")

# Display uploaded images and their metadata (likes, dislikes)
st.write("### TEC SHORT")
uploaded_images = os.listdir('uploads')

if uploaded_images:
    cols = st.columns(3)  # Adjust the number of columns as needed
    for i, image_name in enumerate(uploaded_images):
        image_path = os.path.join("uploads", image_name)
        metadata_path = os.path.join("metadata", image_name + ".json")
        
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
                description = metadata.get("description", "No description available")
                likes = metadata.get("likes", 0)
                dislikes = metadata.get("dislikes", 0)
        else:
            description = "No description available"
            likes, dislikes = 0, 0
        
        # Display image and description in a grid layout
        with cols[i % 3]:  # Use modulo to cycle through columns
            st.image(image_path, caption=description, use_column_width=True)
            st.write(f"**Likes:** {likes}  |  **Dislikes:** {dislikes}")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Like", key=f"like_{image_name}_btn"):
                    if f"like_{image_name}" not in st.session_state:
                        st.session_state[f"like_{image_name}"] = likes
                    st.session_state[f"like_{image_name}"] += 1
                    metadata["likes"] = st.session_state[f"like_{image_name}"]
                    with open(metadata_path, "w") as f:
                        json.dump(metadata, f)
            
            with col2:
                if st.button("Dislike", key=f"dislike_{image_name}_btn"):
                    if f"dislike_{image_name}" not in st.session_state:
                        st.session_state[f"dislike_{image_name}"] = dislikes
                    st.session_state[f"dislike_{image_name}"] += 1
                    metadata["dislikes"] = st.session_state[f"dislike_{image_name}"]
                    with open(metadata_path, "w") as f:
                        json.dump(metadata, f)
else:
    st.write("No images uploaded yet.")
