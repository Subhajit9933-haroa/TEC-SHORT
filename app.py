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
st.title("Photo and Text Uploading Website")
st.write("Upload your photos along with a description!")

# Photo upload widget
uploaded_file = st.file_uploader("Choose a photo...", type=["jpg", "jpeg", "png"])

# Text input widget
description = st.text_area("Enter a description for the photo")

# Button to submit the photo and text
if st.button("Upload"):
    if uploaded_file is not None and description:
        # Save the image
        image_path = os.path.join("uploads", uploaded_file.name)
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Save the description as metadata
        metadata_path = os.path.join("metadata", uploaded_file.name + ".json")
        with open(metadata_path, "w") as f:
            json.dump({"description": description}, f)

        st.success(f"Uploaded and saved: {uploaded_file.name} with description")
    else:
        st.error("Please upload a photo and enter a description.")

# Display uploaded images and their descriptions
st.write("### latest photos")
uploaded_images = os.listdir('uploads')

if uploaded_images:
    for image_name in uploaded_images:
        image_path = os.path.join("uploads", image_name)
        metadata_path = os.path.join("metadata", image_name + ".json")
        
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
                description = metadata.get("description", "No description available")
        else:
            description = "No description available"
        
        # Display image and description
        st.image(image_path, caption=image_name, use_column_width=True)
        st.write(f"**Description**: {description}")
else:
    st.write("No images uploaded yet.")
