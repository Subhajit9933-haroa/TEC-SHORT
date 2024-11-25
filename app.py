import streamlit as st
import json
import os
from datetime import datetime

# Initialize constants
CHAT_FILE = "chat_history.json"
UPLOAD_FOLDER = "uploaded_photos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Ensure chat file exists
if not os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "w") as file:
        json.dump([], file)

# Load chat history
def load_chat():
    with open(CHAT_FILE, "r") as file:
        return json.load(file)

# Save chat history
def save_chat(chat_history):
    with open(CHAT_FILE, "w") as file:
        json.dump(chat_history, file)

# Add a new entry to chat
def add_to_chat(username, message=None, photo=None):
    chat_history = load_chat()
    chat_entry = {
        "username": username,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": message,
        "photo": photo,
    }
    chat_history.append(chat_entry)
    save_chat(chat_history)

# Display chat history
def display_chat():
    chat_history = load_chat()
    for entry in chat_history:
        st.write(f"**{entry['username']}** at *{entry['timestamp']}*")
        if entry["message"]:
            st.write(entry["message"])
        if entry["photo"]:
            st.image(entry["photo"], width=200)
        st.write("---")

# Main app logic
st.title("Group Chat App")
st.sidebar.title("Login")

# Fast login
username = st.sidebar.text_input("Enter your username", "")
if username:
    st.sidebar.success(f"Logged in as {username}")
    st.subheader(f"Welcome, {username}!")

    # Chat input area
    with st.form(key="message_form"):
        message_input = st.text_area("Type your message:")
        submitted = st.form_submit_button("Send")
        if submitted and message_input.strip():
            add_to_chat(username, message=message_input.strip())
            st.experimental_rerun()  # Refresh to show new messages

    # Upload photo area
    with st.form(key="photo_form"):
        uploaded_file = st.file_uploader("Upload a photo:", type=["png", "jpg", "jpeg"])
        photo_submitted = st.form_submit_button("Upload Photo")
        if photo_submitted and uploaded_file:
            photo_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(photo_path, "wb") as file:
                file.write(uploaded_file.getbuffer())
            add_to_chat(username, photo=photo_path)
            st.success("Photo uploaded!")
            st.experimental_rerun()  # Refresh to show new photo

    # Display chat
    st.markdown("### Chat History")
    display_chat()

    # Auto-refresh every 5 seconds
    st.experimental_set_query_params(refresh=1)
else:
    st.sidebar.info("Please log in to start chatting.")
