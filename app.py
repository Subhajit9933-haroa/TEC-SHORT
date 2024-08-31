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
        st.image(image_path, caption=description, use_column_width=True)
        
        # Display Like and Dislike counts
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write(f"👍 {likes} Likes")
            if st.button("Like", key=f"like_{image_name}_btn"):
                if f"like_{image_name}" not in st.session_state:
                    st.session_state[f"like_{image_name}"] = likes
                st.session_state[f"like_{image_name}"] += 1
                metadata["likes"] = st.session_state[f"like_{image_name}"]
                with open(metadata_path, "w") as f:
                    json.dump(metadata, f)
        
        with col2:
            st.write(f"👎 {dislikes} Dislikes")
            if st.button("Dislike", key=f"dislike_{image_name}_btn"):
                if f"dislike_{image_name}" not in st.session_state:
                    st.session_state[f"dislike_{image_name}"] = dislikes
                st.session_state[f"dislike_{image_name}"] += 1
                metadata["dislikes"] = st.session_state[f"dislike_{image_name}"]
                with open(metadata_path, "w") as f:
                    json.dump(metadata, f)

        # Comment section with form handling
        st.write("#### Comments")
        for comment in comments:
            st.write(f"- {comment}")

        with st.form(key=f"comment_form_{image_name}"):
            new_comment = st.text_input("Add a comment", key=f"comment_{image_name}")
            submit_button = st.form_submit_button("Submit Comment")
            if submit_button:
                if new_comment:
                    comments.append(new_comment)
                    metadata["comments"] = comments
                    with open(metadata_path, "w") as f:
                        json.dump(metadata, f)
                    st.experimental_rerun()  # Refresh the page to show updated comments
                else:
                    st.error("Comment cannot be empty.")
else:
    st.write("No images uploaded yet.")
