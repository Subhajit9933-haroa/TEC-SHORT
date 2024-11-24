import streamlit as st

# Title of the app
st.title("Chat App")

# Sidebar for user input
user_name = st.sidebar.text_input("Enter your name")
message = st.sidebar.text_area("Enter your message")

# Initialize session state for storing messages
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Send button
if st.sidebar.button("Send"):
    if user_name and message:
        # Add message to chat history
        st.session_state['messages'].append(f"{user_name}: {message}")
    else:
        st.sidebar.error("Please enter both your name and a message")

# Display chat history
for msg in st.session_state['messages']:
    st.write(msg)
