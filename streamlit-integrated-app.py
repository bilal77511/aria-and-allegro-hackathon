import streamlit as st
import os
import base64
from pathlib import Path
import time
from aria import AriaTextGenerator
from tts import TextToSpeech
from allegro import VideoGenerator
from video_downloader import VideoDownloader
from video_editor import VideoEditor

# Set page configuration
st.set_page_config(
    page_title="Pulse & Prism",
    page_icon="🎥",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        /* Overall theme colors */
        :root {
            --primary-color: #1e88e5;
            --secondary-color: #ff4081;
            --background-color: #f8f9fa;
            --card-background: #ffffff;
        }
        
        /* Main content styling */
        .main {
            background-color: var(--background-color);
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: var(--card-background);
        }
        
        /* Card styling */
        .custom-card {
            background: var(--card-background);
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
            transition: transform 0.3s ease;
        }
        .custom-card:hover {
            transform: translateY(-5px);
        }
        
        /* Button styling */
        .stButton>button {
            width: 100%;
            padding: 0.75rem 1.5rem;
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
            color: white;
            border: none;
            border-radius: 5px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Team member card */
        .team-member {
            background: var(--card-background);
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
            transition: transform 0.3s ease;
        }
        .team-member:hover {
            transform: translateY(-3px);
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: var(--card-background);
            border-radius: 10px;
            padding: 0.5rem;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        
        /* Feature section */
        .feature-section {
            margin: 2rem 0;
            padding: 1.5rem;
            background: var(--card-background);
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Social links */
        .social-link {
            color: var(--primary-color);
            text-decoration: none;
            transition: color 0.3s ease;
        }
        .social-link:hover {
            color: var(--secondary-color);
        }
    </style>
""", unsafe_allow_html=True)

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

# Helper functions
def get_download_link(file_path, link_text):
    with open(file_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}">{link_text}</a>'

def cleanup_files():
    for path in [st.session_state.audio_path, st.session_state.video_path, st.session_state.final_video_path]:
        if path and os.path.exists(path):
            os.remove(path)
    st.session_state.clear()
    st.experimental_rerun()

# Sidebar content
with st.sidebar:
    st.markdown("## 🎭 Pulse & Prism")
    st.markdown("---")
    
    # Configuration Section
    st.markdown("### ⚙️ Configuration")
    poetry_style = st.text_input("Poetry Style", "Enter your desired style (e.g., sad, romantic, spiritual)")
    verses = st.slider("Number of Verses", 1, 5, 2)
    language = st.selectbox("Language", ["english", "urdu"])
    voice = st.selectbox("Voice", ["onyx", "alloy", "echo", "fable", "nova", "shimmer"])
    
    st.markdown("---")
    
    # About Section
    show_about = st.checkbox("Show About", value=False)
    
    if show_about:
        st.markdown("### About Us")
        st.markdown("""
            Transform your poetry into captivating audio-visual experiences using 
            cutting-edge AI technology.
        """)
        
        # Features
        st.markdown("### ✨ Features")
        st.markdown("""
            - 🖋 **AI Poetry Generation**
            - 🎵 **Voice Synthesis**
            - 🎬 **Video Creation**
            - 🎨 **Visual Effects**
        """)
        
        # Team Section
        st.markdown("### 👥 Our Team")
        team_members = [
            ("MUHAMMAD BILAL", "https://github.com/bilal77511", "https://www.linkedin.com/in/muhammad-bilal-a75782280/"),
            ("TIJANI .S. OLALEKAN", "https://github.com/tsolami", "https://www.linkedin.com/in/sotijani/"),
            ("MUHAMMAD IBRAHIM QASMI", "https://github.com/muhammadibrahim313", "https://www.linkedin.com/in/muhammad-ibrahim-qasmi-9876a1297/"),
            ("MUHAMMAD JAWAD", "https://github.com/mj-awad17", "https://www.linkedin.com/in/muhammad-jawad-86507b201/")
        ]
        
        for name, github, linkedin in team_members:
            st.markdown(f"""
                <div class="team-member">
                    <h4>{name}</h4>
                    <a href="{github}" target="_blank" class="social-link">GitHub</a> | 
                    <a href="{linkedin}" target="_blank" class="social-link">LinkedIn</a>
                </div>
            """, unsafe_allow_html=True)
    
    # Clear button at the bottom
    st.markdown("---")
    if st.button("Clear All Files"):
        cleanup_files()

# Main content area
st.title("Poetry Video Generator")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["Generate Poetry", "Create Audio", "Generate Video", "Final Result"])

# Generate Poetry Tab
with tab1:
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
        st.code(st.session_state.generated_poem)

# Create Audio Tab
with tab2:
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

# Generate Video Tab
with tab3:
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
with tab4:
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

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>Created with ❤️ using Streamlit</p>", unsafe_allow_html=True)
