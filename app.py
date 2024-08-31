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
st.title("Photo Uploading Website with Like, Dislike, and Comments")
st.write("Upload your photos along with a description, and interact with other uploads!")

# Photo upload widget
uploaded_file = st.file_uploader("Choose a photo...", type=["jpg", "jpeg", "png"])

# Text input widget for description
description = st.text_area("Enter a description for the photo")

# Button to submit the photo and text
if st.button("Upload"):
    if uploaded_file is not None and description:
        # Save the image
        image_path = os.path.join("uploads", uploaded_file.name)
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Save the description, likes, dislikes, and comments as metadata
        metadata_path = os.path.join("metadata", uploaded_file.name + ".json")
        metadata = {
            "description": description,
            "likes": 0,
            "dislikes": 0,
            "comments": []
        }
        with open(metadata_path, "w") as f:
            json.dump(metadata, f)

        st.success(f"Uploaded and saved: {uploaded_file.name} with description")
    else:
        st.error("Please upload a photo and enter a description.")

# Display uploaded images and their metadata (likes, dislikes, comments)
st.write("### Uploaded Photos with Interactions")
uploaded_images = os.listdir('uploads')

if uploaded_images:
    for image_name in uploaded_images:
        image_path = os.path.join("uploads", image_name)
        metadata_path = os.path.join("metadata", image_name + ".json")
        
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
                description = metadata.get("description", "No description available")
                likes = metadata.get("likes", 0)
                dislikes = metadata.get("dislikes", 0)
                comments = metadata.get("comments", [])
        else:
            description = "No description available"
            likes, dislikes = 0, 0
            comments = []
        
        # Display image and description
        st.image(image_path, caption=image_name, use_column_width=True)
        st.write(f"**Description**: {description}")
        st.write(f"👍 {likes} Likes | 👎 {dislikes} Dislikes")

        # Like and Dislike buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(f"Like {image_name}", key=f"like_{image_name}"):
                likes += 1
                metadata["likes"] = likes
                with open(metadata_path, "w") as f:
                    json.dump(metadata, f)
                st.experimental_rerun()
        with col2:
            if st.button(f"Dislike {image_name}", key=f"dislike_{image_name}"):
                dislikes += 1
                metadata["dislikes"] = dislikes
                with open(metadata_path, "w") as f:
                    json.dump(metadata, f)
                st.experimental_rerun()

        # Comment section
        st.write("#### Comments")
        for comment in comments:
            st.write(f"- {comment}")
        
        new_comment = st.text_input(f"Add a comment for {image_name}", key=f"comment_{image_name}")
        if st.button(f"Submit Comment {image_name}", key=f"submit_comment_{image_name}"):
            if new_comment:
                comments.append(new_comment)
                metadata["comments"] = comments
                with open(metadata_path, "w") as f:
                    json.dump(metadata, f)
                st.experimental_rerun()
            else:
                st.error("Comment cannot be empty.")
else:
    st.write("No images uploaded yet.")
