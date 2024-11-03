# app.py
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

# Custom CSS for styling
st.markdown("""
    <style>
        /* Global theme variables */
        :root {
            --primary-color: #1e88e5;
            --secondary-color: #ff4081;
            --background-color: #f8f9fa;
            --text-color: #333333;
            --card-background: #ffffff;
        }

        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display: none;}

        /* Main container styling */
        .main {
            background: linear-gradient(135deg, var(--background-color) 0%, #ffffff 100%);
            padding: 2rem;
        }

        /* Landing page specific styles */
        .landing-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        .hero-section {
            text-align: center;
            padding: 4rem 0;
            background: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.7));
            border-radius: 20px;
            margin-bottom: 3rem;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }

        .feature-card {
            background: var(--card-background);
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }

        /* Team section styling */
        .team-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }

        .team-member {
            text-align: center;
        }

        .team-member img {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            margin-bottom: 1rem;
            object-fit: cover;
            border: 3px solid var(--primary-color);
        }

        /* Main app styling */
        .stTabs {
            background: var(--card-background);
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .stButton>button {
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 5px;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
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

# Landing page
def show_landing_page():
    st.markdown("""
        <div class="landing-container">
            <div class="hero-section">
                <h1 style="font-size: 3.5rem; color: var(--primary-color);">Pulse & Prism</h1>
                <p style="font-size: 1.2rem; color: var(--text-color); margin: 1.5rem 0;">
                    Transform your poetry into captivating audio-visual experiences using cutting-edge AI technology
                </p>
                <button onclick="handle_get_started()" class="stButton">Get Started</button>
            </div>

            <div class="feature-grid">
                <div class="feature-card">
                    <h3>🖋 AI Poetry Generation</h3>
                    <p>Create unique poems using advanced AI algorithms</p>
                </div>
                <div class="feature-card">
                    <h3>🎵 Voice Synthesis</h3>
                    <p>Convert text to natural-sounding speech</p>
                </div>
                <div class="feature-card">
                    <h3>🎬 Video Creation</h3>
                    <p>Generate stunning visual accompaniments</p>
                </div>
                <div class="feature-card">
                    <h3>🎨 Visual Effects</h3>
                    <p>Add professional effects and transitions</p>
                </div>
            </div>

            <h2 style="text-align: center; margin: 2rem 0;">Our Team</h2>
            <div class="team-grid">
                <div class="team-member">
                    <img src="https://github.com/bilal77511.png" alt="Muhammad Bilal"/>
                    <h3>Muhammad Bilal</h3>
                    <div>
                        <a href="https://github.com/bilal77511" target="_blank">GitHub</a> |
                        <a href="https://linkedin.com/in/muhammad-bilal-a75782280" target="_blank">LinkedIn</a>
                    </div>
                </div>
                <div class="team-member">
                    <img src="https://github.com/tsolami.png" alt="Tijani S. Olalekan"/>
                    <h3>Tijani S. Olalekan</h3>
                    <div>
                        <a href="https://github.com/tsolami" target="_blank">GitHub</a> |
                        <a href="https://linkedin.com/in/sotijani" target="_blank">LinkedIn</a>
                    </div>
                </div>
                <div class="team-member">
                    <img src="https://github.com/muhammadibrahim313.png" alt="Muhammad Ibrahim Qasmi"/>
                    <h3>Muhammad Ibrahim Qasmi</h3>
                    <div>
                        <a href="https://github.com/muhammadibrahim313" target="_blank">GitHub</a> |
                        <a href="https://linkedin.com/in/muhammad-ibrahim-qasmi-9876a1297" target="_blank">LinkedIn</a>
                    </div>
                </div>
                <div class="team-member">
                    <img src="https://github.com/mj-awad17.png" alt="Muhammad Jawad"/>
                    <h3>Muhammad Jawad</h3>
                    <div>
                        <a href="https://github.com/mj-awad17" target="_blank">GitHub</a> |
                        <a href="https://linkedin.com/in/muhammad-jawad-86507b201" target="_blank">LinkedIn</a>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Continue to App"):
        st.session_state.page = 'main'
        st.experimental_rerun()

# Main application
def show_main_app():
    # Sidebar
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
        if st.button("Back to Home"):
            st.session_state.page = 'landing'
            st.experimental_rerun()
        
        if st.button("Clear All Files"):
            cleanup_files()

    # Main content
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
            st.markdown(f"\n{st.session_state.generated_poem}\n")

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

# Main execution
def main():
    if st.session_state.page == 'landing':
        show_landing_page()
    else:
        show_main_app()

if __name__ == "__main__":
    main()
