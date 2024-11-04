import streamlit as st
from pathlib import Path
import time
import os
import base64
from aria import AriaTextGenerator
from tts import TextToSpeech
from allegro import VideoGenerator
from video_downloader import VideoDownloader
from video_editor import VideoEditor

def load_css():
    st.markdown("""
    <style>
    .stApp {
        background-color: #0D0D0D;
        color: #F2DFF2;
    }
    .main-title {
        color: #763DF2;
        font-size: 72px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .tagline {
        color: #5129A6;
        font-size: 28px;
        font-style: italic;
        text-align: center;
        margin-bottom: 30px;
    }
    .stTabs {
        margin-top: 30px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #421E59;
        padding: 10px 20px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #5129A6;
        color: #F2DFF2;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #763DF2;
        transform: translateY(-2px);
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #763DF2;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
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
    .stSelectbox select {
        background-color: #421E59;
        color: #F2DFF2;
    }
    </style>
    """, unsafe_allow_html=True)

def get_download_link(file_path, link_text):
    with open(file_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}">{link_text}</a>'

def cleanup_files():
    if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
        os.remove(st.session_state.audio_path)
    if st.session_state.video_path and os.path.exists(st.session_state.video_path):
        os.remove(st.session_state.video_path)
    if st.session_state.final_video_path and os.path.exists(st.session_state.final_video_path):
        os.remove(st.session_state.final_video_path)

def main():
    load_css()
    
    # Initialize session state
    if 'generated_poem' not in st.session_state:
        st.session_state.generated_poem = None
    if 'audio_path' not in st.session_state:
        st.session_state.audio_path = None
    if 'video_path' not in st.session_state:
        st.session_state.video_path = None
    if 'final_video_path' not in st.session_state:
        st.session_state.final_video_path = None

    # Initialize components
    @st.cache_resource
    def initialize_components():
        return {
            'aria': AriaTextGenerator(),
            'tts': TextToSpeech(),
            'video': VideoGenerator(),
            'downloader': VideoDownloader(),
            'editor': VideoEditor()
        }

    components = initialize_components()
    
    
    st.markdown("<h1 class='main-title'>Pulse & Prism</h1>", unsafe_allow_html=True)
    st.markdown("<p class='tagline'> Generate beautiful poetry and transform them into videos with background music.</p>", unsafe_allow_html=True)

    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        poetry_style = st.text_input(
            "Poetry Style",
            value="",
            placeholder="Enter your desired style (e.g., sad, romantic, spiritual)"
        )
        verses = st.slider("Number of Verses", 1, 5, 2)
        language = st.selectbox("Language", ["english", "urdu"])
        voice = st.selectbox("Voice", ["onyx", "alloy", "echo", "fable", "nova", "shimmer"])

    # Main content tabs
    tabs = st.tabs(["Generate Poetry", "Create Audio", "Generate Video", "Final Result"])

    # Poetry Generation Tab
    with tabs[0]:
        st.header("1. Generate Poetry")
        generate_button = st.button("Generate Poetry")
        
        if generate_button:
            if not poetry_style.strip():
                st.error("Please enter a poetry style")
            else:
                with st.spinner("Generating Using Aria..."):
                    try:
                        st.session_state.generated_poem = components['aria'].generate_poem(
                            style=poetry_style,
                            verses=verses,
                            language=language
                        )
                        st.success("Poetry generated successfully!")
                    except Exception as e:
                        st.error(f"Error generating poem: {str(e)}")
        
        if st.session_state.generated_poem:
            st.markdown("### Generated Poetry")
            st.code(st.session_state.generated_poem)

    # Audio Generation Tab
    with tabs[1]:
        st.header("2. Create Audio")
        if st.session_state.generated_poem:
            if st.button("Generate Audio"):
                with st.spinner("Generating audio..."):
                    try:
                        st.session_state.audio_path = components['tts'].generate_speech(
                            text=st.session_state.generated_poem,
                            filename="generated_poem.mp3",
                            voice=voice
                        )
                        st.success("Audio generated successfully!")
                    except Exception as e:
                        st.error(f"Error generating audio: {str(e)}")
            
            if st.session_state.audio_path:
                st.audio(str(st.session_state.audio_path))
                st.markdown(get_download_link(st.session_state.audio_path, "Download Audio"), unsafe_allow_html=True)
        else:
            st.warning("Please generate a poem first.")

    # Video Generation Tab
    with tabs[2]:
        st.header("3. Generate Video")
        if st.session_state.audio_path:
            video_prompt = st.text_area(
                "Video Prompt",
                f"A serene natural scene with gentle movements, perfect for poetry background \n the poetry is {st.session_state.generated_poem}"
            )
            
            if st.button("Generate Video"):
                if not video_prompt.strip():
                    st.error("Please enter a video prompt")
                else:
                    with st.spinner("Initiating video generation..."):
                        try:
                            request_id, video_url = components['video'].create_video(
                                prompt=video_prompt,
                                wait_for_completion=True
                            )
                            
                            if video_url:
                                video_path = components['downloader'].download_video(
                                    url=video_url,
                                    filename="poetry_background.mp4"
                                )
                                st.session_state.video_path = video_path
                                st.success("Video generated and downloaded successfully!")
                                st.markdown(get_download_link(video_path, "Download Raw Video"), unsafe_allow_html=True)
                            
                        except Exception as e:
                            st.error(f"Error with video: {str(e)}")
        else:
            st.warning("Please generate audio first.")

    # Final Result Tab
    with tabs[3]:
        st.header("4. Final Result")
        if st.session_state.video_path and st.session_state.audio_path:
            if st.button("Create Final Video"):
                with st.spinner("Creating final video with effects..."):
                    try:
                        output_path = "final_poetry_video.mp4"
                        final_path = components['editor'].create_video_with_audio(
                            video_path=str(st.session_state.video_path),
                            audio_path=str(st.session_state.audio_path),
                            output_path=output_path
                        )
                        st.session_state.final_video_path = final_path
                        st.success("Final video created successfully!")
                    except Exception as e:
                        st.error(f"Error creating final video: {str(e)}")
            
            if st.session_state.final_video_path:
                st.video(str(st.session_state.final_video_path))
                st.markdown(get_download_link(st.session_state.final_video_path, "Download Final Video"), unsafe_allow_html=True)
        else:
            st.warning("Please generate video and audio first.")

    # Cleanup button
    if st.sidebar.button("Clear All Files"):
        cleanup_files()
        for key in ['generated_poem', 'audio_path', 'video_path', 'final_video_path']:
            if key in st.session_state:
                st.session_state[key] = None
        st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("Created with ❤️ by B-TAJI Crew")

if __name__ == "__main__":
    st.set_page_config(
        page_title="Poetry Video Generator",
        page_icon="🎥",
        layout="wide"
    )
    main()