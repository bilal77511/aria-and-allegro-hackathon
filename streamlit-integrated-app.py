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

# Set page config
st.set_page_config(
    page_title="DataVue | Poetry Generator",
    page_icon="🎥",
    layout="wide"
)

# Load CSS styles
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
    .sidebar-nav {
        padding: 10px;
        background-color: #e6f2ff;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Helper Functions
def get_download_link(file_path, link_text):
    """Create a download link for files"""
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        return f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}">{link_text}</a>'
    except Exception as e:
        st.error(f"Error creating download link: {str(e)}")
        return None

def cleanup_files():
    """Clean up generated files"""
    try:
        for key in ['audio_path', 'video_path', 'final_video_path']:
            if key in st.session_state and st.session_state[key] and os.path.exists(st.session_state[key]):
                os.remove(st.session_state[key])
        st.session_state.clear()
    except Exception as e:
        st.error(f"Error cleaning up files: {str(e)}")

# Initialize components
@st.cache_resource
def initialize_components():
    """Initialize all required components"""
    try:
        return {
            'aria': AriaTextGenerator(),
            'tts': TextToSpeech(),
            'video': VideoGenerator(),
            'downloader': VideoDownloader(),
            'editor': VideoEditor()
        }
    except Exception as e:
        st.error(f"Error initializing components: {str(e)}")
        return None

def show_landing_page():
    """Display the landing page"""
    st.markdown("<h1 class='main-title'>📊 DataVue 🔍</h1>", unsafe_allow_html=True)
    st.markdown("<p class='tagline'>\"Your Data, Your View\" 🚀</p>", unsafe_allow_html=True)

    st.markdown("""
    <div class='feature-box'>
        <p class='feature-title'>🎭 AI Poetry Generator</p>
        <p>Transform your ideas into beautiful poems with our AI-powered poetry generator. 
        Create stunning videos with background music and visuals that match your poetry.</p>
    </div>
    """, unsafe_allow_html=True)

    # Other features from your original landing page...
    features = [
        {
            "title": "🔬 Complete Data Analysis",
            "description": "Experience effortless data analysis with DataVue."
        },
        {
            "title": "🤖 AI Assistant",
            "description": "Access a powerful AI assistant for all your data science tasks."
        },
        {
            "title": "📊 Automated EDA",
            "description": "Generate in-depth reports and visualizations with just a few clicks."
        }
    ]

    for feature in features:
        st.markdown(f"""
        <div class='feature-box'>
            <p class='feature-title'>{feature['title']}</p>
            <p>{feature['description']}</p>
        </div>
        """, unsafe_allow_html=True)

def show_poetry_generator():
    """Display the poetry generator interface"""
    st.title("🎭 Poetry Video Generator")
    
    # Initialize session state
    for key in ['generated_poem', 'audio_path', 'video_path', 'final_video_path']:
        if key not in st.session_state:
            st.session_state[key] = None

    components = initialize_components()
    if not components:
        st.error("Failed to initialize components. Please try again.")
        return

    # Create tabs
    tabs = st.tabs(["Generate Poetry", "Create Audio", "Generate Video", "Final Result"])

    with tabs[0]:
        st.header("1. Generate Poetry")
        try:
            if st.button("Generate Poem"):
                with st.spinner("Generating poem..."):
                    st.session_state.generated_poem = components['aria'].generate_poem(
                        style=st.session_state.get('poetry_style', 'romantic'),
                        verses=st.session_state.get('verses', 2),
                        language=st.session_state.get('language', 'english')
                    )
                    st.success("Poem generated successfully!")
            
            if st.session_state.generated_poem:
                st.markdown("### Generated Poem")
                st.code(st.session_state.generated_poem)
        except Exception as e:
            st.error(f"Error in poetry generation: {str(e)}")

    # Similar error handling for other tabs...
    # (Audio, Video, and Final Result tabs implementation remains the same but with added error handling)

def main():
    """Main application function"""
    load_css()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("<div class='sidebar-nav'>", unsafe_allow_html=True)
        st.title("Navigation")
        
        # Poetry Generator Configuration
        if st.button("Show Poetry Generator"):
            st.session_state['show_generator'] = True
            st.header("Poetry Configuration")
            st.session_state['poetry_style'] = st.text_input("Poetry Style", "romantic")
            st.session_state['verses'] = st.slider("Number of Verses", 1, 5, 2)
            st.session_state['language'] = st.selectbox("Language", ["english", "urdu"])
            st.session_state['voice'] = st.selectbox("Voice", ["onyx", "alloy", "echo", "fable", "nova", "shimmer"])
            
            if st.button("Clear All Files"):
                cleanup_files()
                st.success("All files cleared successfully!")
                st.experimental_rerun()
        else:
            st.session_state['show_generator'] = False
        st.markdown("</div>", unsafe_allow_html=True)

    # Main content area
    if st.session_state.get('show_generator', False):
        show_poetry_generator()
    else:
        show_landing_page()

if __name__ == "__main__":
    main()