import streamlit as st
from PIL import Image
import os

# Create a folder to store uploaded images
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Streamlit title and description
st.title("Photo Uploading Website")
st.write("Upload your photos here!")

# Photo upload widget
uploaded_file = st.file_uploader("Choose a photo...", type=["jpg", "jpeg", "png"])

# If a file is uploaded
if uploaded_file is not None:
    # Open the image
    image = Image.open(uploaded_file)
    
    # Display the image
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Save the image
    save_path = os.path.join("uploads", uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"Saved file: {uploaded_file.name}")

# Show uploaded images
st.write("### Uploaded Images")
uploaded_images = os.listdir('uploads')

if uploaded_images:
    for image_name in uploaded_images:
        image_path = os.path.join("uploads", image_name)
        st.image(image_path, caption=image_name, use_column_width=True)
else:
    st.write("No images uploaded yet.")
