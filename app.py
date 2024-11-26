import streamlit as st
from datetime import datetime

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Sidebar for chat list
st.sidebar.title("Chats")
st.sidebar.write("Contact 1")
st.sidebar.write("Contact 2")

# Main Chat UI
st.title("Chat (WhatsApp-like)")

# Display messages
st.write("### Messages")
for msg in st.session_state["messages"]:
    sender, text, timestamp = msg
    if sender == "You":
        # User messages on the right
        st.markdown(
            f"""
            <div style='text-align: right; background: #dcf8c6; padding: 10px; border-radius: 10px; margin: 5px;'>
                <b>{sender}:</b> {text} <br><small>{timestamp}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Others' messages on the left
        st.markdown(
            f"""
            <div style='text-align: left; background: #fff; padding: 10px; border-radius: 10px; margin: 5px;'>
                <b>{sender}:</b> {text} <br><small>{timestamp}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Input box for sending messages
text_input = st.text_input("Type your message", placeholder="Type a message...")

if st.button("Send"):
    if text_input.strip():
        # Append user message
        st.session_state["messages"].append(("You", text_input, datetime.now().strftime("%H:%M")))
        # Simulate a reply
        st.session_state["messages"].append(
            ("Friend", "Got your message!", datetime.now().strftime("%H:%M"))
        )
        st.experimental_rerun()
