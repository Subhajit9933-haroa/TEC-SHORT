import streamlit as st

# Title of the web application
st.title("Form Fill-Up Application")

# Subheader
st.subheader("Please fill out the form below:")

# Form
with st.form("user_form"):
    # Input fields
    name = st.text_input("Full Name", placeholder="Enter your name")
    email = st.text_input("Email", placeholder="Enter your email")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender", options=["Select", "Male", "Female", "Other"])
    country = st.text_input("Country", placeholder="Enter your country")
    feedback = st.text_area("Feedback", placeholder="Enter your feedback here...")
    
    # Submit button
    submit_button = st.form_submit_button("Submit")

# Display submitted data
if submit_button:
    if name and email and gender != "Select":
        st.success("Form submitted successfully!")
        st.write("### Submitted Information")
        st.write(f"**Name:** {name}")
        st.write(f"**Email:** {email}")
        st.write(f"**Age:** {age}")
        st.write(f"**Gender:** {gender}")
        st.write(f"**Country:** {country}")
        st.write(f"**Feedback:** {feedback}")
    else:
        st.error("Please fill in all required fields (Name, Email, and Gender).")
