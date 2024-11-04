import streamlit as st
from tts import TextToSpeech
from allegro import VideoGenerator
from video_downloader import VideoDownloader
import os
import base64

def load_css():
    st.markdown("""
    <style>
    .stApp {
        background-color: #0D0D0D;
        color: #F2DFF2;
    }
    .main-title {
        color: #763DF2;
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .tagline {
        color: #5129A6;
        font-size: 24px;
        font-style: italic;
        text-align: center;
        margin-bottom: 30px;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: #421E59;
        color: #F2DFF2;
        border: 1px solid #5129A6;
    }
    .stButton button {
        background-color: #5129A6;
        color: #F2DFF2;
        border: none;
    }
    .stButton button:hover {
        background-color: #763DF2;
    }
    </style>
    """, unsafe_allow_html=True)

def get_download_link(file_path, link_text):
    with open(file_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}">{link_text}</a>'

def main():
    st.set_page_config(page_title="Custom Content Generator", page_icon="📹", layout="wide")
    load_css()
    
    st.markdown("<h1 class='main-title'>📹 Custom Content Generator</h1>", unsafe_allow_html=True)
    st.markdown("<p class='tagline'>Create custom audio and videos from your text</p>", unsafe_allow_html=True)
    
    # Initialize session state
    if 'audio_path' not in st.session_state:
        st.session_state.audio_path = None
    if 'video_path' not in st.session_state:
        st.session_state.video_path = None
    
    # Add cleanup function
    def cleanup_files():
        if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
            os.remove(st.session_state.audio_path)
        if st.session_state.video_path and os.path.exists(st.session_state.video_path):
            os.remove(st.session_state.video_path)
    
    # Initialize components
    @st.cache_resource
    def initialize_components():
        return {
            'tts': TextToSpeech(),
            'video': VideoGenerator(),
            'downloader': VideoDownloader()
        }
    
    components = initialize_components()

    # Define the voice options
    voices = {"Onyx": "onyx", "Alloy": "alloy", "Echo": "echo", "Fable": "fable", "Nova": "nova", "Shimmer": "shimmer"}
    
    # Text input section
    st.header("Enter Your Text")
    user_text = st.text_area("Your Text", height=150, 
                            placeholder="Enter the text you want to convert to speech...")
    voice = st.selectbox("Select Voice", list(voices.keys()))
    
    # Audio generation section
    st.header("Generate Audio")
    if st.button("Create Audio") and user_text:
        with st.spinner("Generating audio..."):
            try:
                audio_path = components['tts'].generate_speech(
                    text=user_text,
                    filename="custom_audio.mp3",
                    voice=voices[voice]
                )
                st.session_state.audio_path = str(audio_path)
                st.success("Audio generated successfully!")
            except Exception as e:
                st.error(f"Error generating audio: {str(e)}")
    
    # Display audio if available
    if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
        st.audio(st.session_state.audio_path)
        st.markdown(get_download_link(st.session_state.audio_path, "Download Audio"), unsafe_allow_html=True)
    
    # Video generation section
    st.header("Generate Video (Optional)")
    video_prompt = st.text_area("Video Description", 
        placeholder="Describe the video scene you want to generate...",
        help="Describe the visual scene you want for your video background")
    
    if st.button("Create Video") and video_prompt:
        with st.spinner("Generating video (this may take a few minutes)..."):
            try:
                request_id, video_url = components['video'].create_video(
                    prompt=video_prompt,
                    wait_for_completion=True
                )
                
                if video_url:
                    video_path = components['downloader'].download_video(
                        url=video_url,
                        filename="custom_video.mp4"
                    )
                    st.session_state.video_path = str(video_path)
                    st.success("Video generated successfully!")
            except Exception as e:
                st.error(f"Error generating video: {str(e)}")
    
    # Display video if available
    if st.session_state.video_path and os.path.exists(st.session_state.video_path):
        st.video(st.session_state.video_path)
        st.markdown(get_download_link(st.session_state.video_path, "Download Video"), unsafe_allow_html=True)
    
    # Cleanup button in sidebar
    if st.sidebar.button("Clear All Files"):
        cleanup_files()
        st.session_state.audio_path = None
        st.session_state.video_path = None
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("Created with ❤️ by B-TAJI Crew")

if __name__ == "__main__":
    main()
