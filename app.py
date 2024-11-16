import streamlit as st
import json
import os

# User credentials for login
USER_EMAIL = "subhajitsadhukhan816@gmail.com"
USER_PASSWORD = "Subhajit8167@"

# Data file to store submitted form data
DATA_FILE = "data.json"

# Load existing data or initialize an empty list
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as file:
        form_data = json.load(file)
else:
    form_data = []

# Sidebar for login
st.sidebar.title("Login")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Login form
    with st.sidebar.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

    # Login validation
    if login_button:
        if email == USER_EMAIL and password == USER_PASSWORD:
            st.session_state.logged_in = True
            st.sidebar.success("Logged in successfully!")
        else:
            st.sidebar.error("Invalid email or password.")
else:
    st.sidebar.success("You are logged in.")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()

# Main content
if st.session_state.logged_in:
    # Display all previous forms
    st.title("Submitted Forms")
    if form_data:
        for idx, entry in enumerate(form_data, 1):
            st.write(f"### Form {idx}")
            for key, value in entry.items():
                st.write(f"**{key.capitalize()}**: {value}")
            st.write("---")
    else:
        st.info("No forms submitted yet.")

else:
    # Form submission
    st.title("Form Fill-Up Application")
    st.subheader("Please fill out the form below:")

    with st.form("user_form"):
        name = st.text_input("Full Name", placeholder="Enter your name")
        email = st.text_input("Email", placeholder="Enter your email")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        gender = st.selectbox("Gender", options=["Select", "Male", "Female", "Other"])
        country = st.text_input("Country", placeholder="Enter your country")
        feedback = st.text_area("Feedback", placeholder="Enter your feedback here...")
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        if name and email and gender != "Select":
            # Save form data
            form_entry = {
                "name": name,
                "email": email,
                "age": age,
                "gender": gender,
                "country": country,
                "feedback": feedback,
            }
            form_data.append(form_entry)

            # Save data to file
            with open(DATA_FILE, "w") as file:
                json.dump(form_data, file)

            st.success("Form submitted successfully!")
        else:
            st.error("Please fill in all required fields (Name, Email, and Gender).")
