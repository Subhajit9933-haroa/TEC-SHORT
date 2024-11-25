import streamlit as st
import json
from datetime import datetime
import os

# File paths
USER_DB = "user_db.json"
CHAT_HISTORY = "chat_history.json"

# Initialize files if they don't exist
if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump({}, f)

if not os.path.exists(CHAT_HISTORY):
    with open(CHAT_HISTORY, "w") as f:
        json.dump([], f)


# Helper functions
def load_users():
    with open(USER_DB, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)


def load_chat():
    with open(CHAT_HISTORY, "r") as f:
        return json.load(f)


def save_chat(chat):
    with open(CHAT_HISTORY, "w") as f:
        json.dump(chat, f)


# Authentication
def login(username, password):
    users = load_users()
    if username in users and users[username] == password:
        return True
    return False


def sign_up(username, password):
    users = load_users()
    if username in users:
        return False  # Username already exists
    users[username] = password
    save_users(users)
    return True


# Chat system
def add_message(username, message, image=None):
    chat = load_chat()
    chat.append({
        "username": username,
        "message": message,
        "image": image,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_chat(chat)


def display_chat():
    chat = load_chat()
    for entry in chat:
        st.markdown(f"**{entry['username']}** *({entry['timestamp']})*")
        if entry["message"]:
            st.markdown(entry["message"])
        if entry["image"]:
            st.image(entry["image"], use_column_width=True)
        st.markdown("---")


# Streamlit app
st.set_page_config(page_title="Group Chat", page_icon="💬", layout="wide")

# State management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Sidebar login/signup
st.sidebar.title("Authentication")
if not st.session_state.logged_in:
    auth_action = st.sidebar.radio("Choose an action", ["Login", "Sign Up"])

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if auth_action == "Login":
        if st.sidebar.button("Log In"):
            if login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.sidebar.success(f"Welcome back, {username}!")
            else:
                st.sidebar.error("Invalid username or password.")

    elif auth_action == "Sign Up":
        if st.sidebar.button("Sign Up"):
            if sign_up(username, password):
                st.sidebar.success("Sign-up successful! Please log in.")
            else:
                st.sidebar.error("Username already exists.")
else:
    st.sidebar.success(f"Logged in as {st.session_state.username}")
    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.username = ""

# Main chat interface
if st.session_state.logged_in:
    st.title("💬 Group Chat")
    st.markdown(f"Welcome, **{st.session_state.username}**!")

    # Chat messages
    st.subheader("Chat Messages")
    display_chat()

    # Message input
    st.subheader("Send a Message")
    message = st.text_area("Type your message here", height=100)
    uploaded_image = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg"])

    if st.button("Send"):
        if message or uploaded_image:
            image_path = None
            if uploaded_image:
                image_path = f"uploads/{uploaded_image.name}"
                with open(image_path, "wb") as f:
                    f.write(uploaded_image.getbuffer())

            add_message(st.session_state.username, message, image=image_path)
            st.experimental_rerun()
        else:
            st.error("Please enter a message or upload an image.")
else:
    st.title("Welcome to Group Chat!")
    st.markdown("Please log in or sign up to join the chat.")
