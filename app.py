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

import streamlit as st
from streamlit.components.v1 import html

def load_css():
    st.markdown("""
    <style>
    .stApp {
        background-color: #f0f8ff;
    }
    .main-title {
        color: #1e90ff;
        font-size: 72px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .tagline {
        color: #4169e1;
        font-size: 28px;
        font-style: italic;
        text-align: center;
        margin-bottom: 30px;
    }
    .section-header {
        color: #1e90ff;
        font-size: 36px;
        font-weight: bold;
        margin-top: 40px;
        margin-bottom: 20px;
        text-align: center;
    }
    .feature-box {
        background-color: #e6f2ff;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        transition: transform 0.3s ease-in-out;
    }
    .feature-box:hover {
        transform: scale(1.05);
    }
    .feature-title {
        color: #4169e1;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .app-button {
        background-color: #1e90ff;
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 12px 24px;
        border-radius: 25px;
        text-align: center;
        margin: 10px;
        display: inline-block;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    .app-button:hover {
        background-color: #4169e1;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .problem-statement {
        background-color: #ffd700;
        border-radius: 10px;
        padding: 20px;
        margin: 30px 0;
        text-align: center;
        font-size: 20px;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    load_css()

    # Main title and tagline with emojis
    st.markdown("<h1 class='main-title'>📊 DataVue 🔍</h1>", unsafe_allow_html=True)
    st.markdown("<p class='tagline'>\"Your Data, Your View\" 🚀</p>", unsafe_allow_html=True)

    # Problem Statement
    st.markdown("""
    <div class='problem-statement'>
        <h3>🤔 Struggling with data analysis?</h3>
        <p>Drowning in data but starving for insights? Tired of complex tools and steep learning curves?</p>
        <h3>💡 DataVue is your solution!</h3>
    </div>
    """, unsafe_allow_html=True)

    # Why choose DataVue section
    st.markdown("<h2 class='section-header'>🌟 Why Choose DataVue?</h2>", unsafe_allow_html=True)

    features = [
        {
            "title": "🔬 Complete Data Analysis",
            "description": "Experience effortless data analysis with DataVue. Simply provide your data, and let our advanced algorithms handle the rest, delivering comprehensive insights at your fingertips."
        },
        {
            "title": "🤖 AI Assistant for Data Science",
            "description": "Access a powerful AI assistant dedicated to all your data science tasks. Get instant help, explanations, and curated resources to supercharge your data science journey."
        },
        {
            "title": "📊 Automated EDA",
            "description": "Unlock the power of automated Exploratory Data Analysis (EDA) with SweetViz and Pandas Profiling. Generate in-depth reports and visualizations with just a few clicks, saving you time and effort."
        },
        {
            "title": "📚 Comprehensive Learning Resources",
            "description": "Embark on a data science learning adventure from zero to hero. Access a wealth of study materials covering EDA, missing value handling, feature engineering, scaling transformations, and ML algorithms - all in one place, complete with example datasets and practical demos."
        }
    ]

    for feature in features:
        st.markdown(f"""
        <div class='feature-box'>
            <p class='feature-title'>{feature['title']}</p>
            <p>{feature['description']}</p>
        </div>
        """, unsafe_allow_html=True)

    # Demo video
    st.markdown("<h2 class='section-header'>🎥 See DataVue in Action</h2>", unsafe_allow_html=True)
    
    # Embed YouTube video using Streamlit's built-in method
    st.video("https://www.youtube.com/embed/4eHreET_XYA")


    # Main apps
    st.markdown("<h2 class='section-header'>🚀 Explore DataVue</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("<a href='/data_analysis' target='_self' class='app-button'>📈 Data Analysis</a>", unsafe_allow_html=True)
    with col2:
        st.markdown("<a href='/ai_assistant' target='_self' class='app-button'>🤖 AI Assistant</a>", unsafe_allow_html=True)
    with col3:
        st.markdown("<a href='/auto_eda' target='_self' class='app-button'>🔍 Auto EDA</a>", unsafe_allow_html=True)
    with col4:
        st.markdown("<a href='/learning_resources' target='_self' class='app-button'>📚 Learning Resources</a>", unsafe_allow_html=True)

    # GitHub and Demo links
    st.markdown("<h2 class='section-header'>🌐 Connect with DataVue</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<a href='https://github.com/yourusername/datavue' target='_blank' class='app-button'>👨‍💻 GitHub Repository</a>", unsafe_allow_html=True)
    with col2:
        st.markdown("<a href='https://demo.datavue.com' target='_blank' class='app-button'>🖥 Live Demo</a>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

# Set page config
st.set_page_config(
    page_title="Poetry Video Generator",
    page_icon="🎥",
    layout="wide"
)

# Function to create download button
def get_download_link(file_path, link_text):
    with open(file_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}">{link_text}</a>'

# Function to clean up files
def cleanup_files():
    if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
        os.remove(st.session_state.audio_path)
    if st.session_state.video_path and os.path.exists(st.session_state.video_path):
        os.remove(st.session_state.video_path)
    if st.session_state.final_video_path and os.path.exists(st.session_state.final_video_path):
        os.remove(st.session_state.final_video_path)

# Initialize the session state
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

# Main title
st.title("🎭 Poetry Video Generator")
st.markdown("Generate beautiful poems and transform them into videos with background music.")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    poetry_style = st.text_input("Poetry Style", "Enter your desired style (e.g., sad, romantic, spiritual)")
    verses = st.slider("Number of Verses", 1, 5, 2)
    language = st.selectbox("Language", ["english", "urdu"])
    voice = st.selectbox("Voice", ["onyx", "alloy", "echo", "fable", "nova", "shimmer"])

# Main content area
tabs = st.tabs(["Generate Poetry", "Create Audio", "Generate Video", "Final Result"])

# Poetry Generation Tab
with tabs[0]:
    st.header("1. Generate Poetry")
    if st.button("Generate Poem"):
        with st.spinner("Generating poem..."):
            try:
                st.session_state.generated_poem = components['aria'].generate_poem(
                    style=poetry_style,
                    verses=verses,
                    language=language
                )
                st.success("Poem generated successfully!")
            except Exception as e:
                st.error(f"Error generating poem: {str(e)}")
    
    if st.session_state.generated_poem:
        st.markdown("### Generated Poem")
        st.markdown(f"```\n{st.session_state.generated_poem}\n```")
        # Add copy button for poem
        st.markdown("Copy poem to clipboard:")
        st.code(st.session_state.generated_poem)

# Audio Generation Tab
with tabs[1]:
    st.header("2. Create Audio")
    if st.session_state.generated_poem:
        if st.button("Generate Audio"):
            with st.spinner("Generating audio..."):
                try:
                    # Use consistent filename
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
            with st.spinner("Initiating video generation..."):
                try:
                    request_id, video_url = components['video'].create_video(
                        prompt=video_prompt,
                        wait_for_completion=True
                    )
                    
                    if video_url:
                        # Download with consistent filename
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
                    # Use consistent filename
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
    st.session_state.clear()
    st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit")