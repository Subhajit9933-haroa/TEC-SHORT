import streamlit as st

# Set page configuration
st.set_page_config(page_title="TikTok-Inspired Video Player", layout="centered")

# Custom CSS for TikTok-style layout and color scheme
st.markdown(
    """
    <style>
    body {
        background-color: #141414;
        color: white;
        font-family: 'Arial', sans-serif;
    }
    .video-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100vh;
        max-width: 400px; /* Mobile screen width */
        background-color: #222;
        border-radius: 15px;
        overflow: hidden;
    }
    video {
        width: 100%;
        height: auto;
        border-radius: 15px;
    }
    .control-bar {
        margin-top: 15px;
        display: flex;
        justify-content: space-between;
        width: 100%;
        max-width: 400px; /* Align with the video frame */
    }
    button {
        background-color: #FE2C55;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 20px;
        font-size: 16px;
        cursor: pointer;
    }
    button:hover {
        background-color: #FF5C75;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.title("🎥 TikTok-Inspired Video Player")

# State to store videos
if "videos" not in st.session_state:
    st.session_state["videos"] = []  # Store uploaded videos

# Upload Section
st.subheader("Upload a Video")
uploaded_video = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])
if uploaded_video:
    st.session_state["videos"].append(uploaded_video)

# Show Uploaded Videos
if st.session_state["videos"]:
    video_index = st.session_state.get("video_index", 0)

    # Display the current video in a mobile-sized frame
    st.markdown('<div class="video-container">', unsafe_allow_html=True)
    st.video(st.session_state["videos"][video_index])
    st.markdown('</div>', unsafe_allow_html=True)

    # Controls
    st.markdown('<div class="control-bar">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Previous"):
            video_index = (video_index - 1) % len(st.session_state["videos"])
            st.session_state["video_index"] = video_index
    with col2:
        if st.button("🔄 Reload"):
            st.experimental_rerun()
    with col3:
        if st.button("➡️ Next"):
            video_index = (video_index + 1) % len(st.session_state["videos"])
            st.session_state["video_index"] = video_index

    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.write("No videos uploaded yet. Upload a video to get started!")
