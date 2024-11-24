import streamlit as st

# Initialize chat data and images
if "chat_data" not in st.session_state:
    st.session_state.chat_data = []  # Stores chat messages and images

# Function to display messages
def display_chat():
    for entry in st.session_state.chat_data:
        if entry["type"] == "text":
            st.write(f"**User:** {entry['content']}")
        elif entry["type"] == "image":
            st.image(entry["content"], caption="Uploaded Image", use_column_width=True)

# Title
st.title("Group Chat and Photo Upload")

# Chat Input
with st.form("chat_form"):
    message = st.text_input("Type your message:")
    submitted = st.form_submit_button("Send")
    if submitted and message.strip():
        st.session_state.chat_data.append({"type": "text", "content": message})
        st.experimental_rerun()

# Image Upload
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
if uploaded_image is not None:
    st.session_state.chat_data.append({"type": "image", "content": uploaded_image})
    st.experimental_rerun()

# Display chat
st.subheader("Chat Messages")
display_chat()
