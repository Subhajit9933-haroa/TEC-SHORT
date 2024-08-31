import streamlit as st
from PIL import Image
import os

# Function to create the layout of a single post
def post_area(uploaded_image_path=None):
    st.write("---")
    st.write("**User Name**")
    if uploaded_image_path:
        st.image(uploaded_image_path, caption="Uploaded image.", use_column_width=True)
    else:
        st.image("post_image.jpg", caption="This is a post image.", use_column_width=True)
    st.write("This is a sample post. It mimics the Facebook post style.")
    st.write("#### Comments")
    st.text_area("Write a comment...", key="comment" + str(st.session_state.get('post_id', 0)))
    st.session_state.post_id += 1  # Increment post ID for unique comment boxes

# Main function to structure the page
def main():
    st.session_state.post_id = 0  # Initialize post ID for comments

    # Sidebar for Login
    with st.sidebar:
        st.image("TEC SHORT_logo.png", width=200)
        st.write("### Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            st.success(f"Welcome {username}!")
            st.write("## Logged in as:", username)
        else:
            st.write("Please log in to continue.")

    # Header
    st.title("TEC SHORT")
    st.subheader("WELLCOME TO TEC SHORT WEB PAGE")

    # Top Navigation Bar
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Home")
    with col2:
        st.button("Friends")
    with col3:
        st.button("Messages")

    # Upload Image Option
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Save uploaded image to local directory
        uploaded_image_path = os.path.join(os.getcwd(), uploaded_file.name)
        with open(uploaded_image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Image uploaded and saved successfully!")
    else:
        uploaded_image_path = None

    # Main Content Area (News Feed)
    st.write("### News Feed")
    for i in range(5):  # Generate multiple posts
        post_area(uploaded_image_path)

if __name__ == "__main__":
    main()
