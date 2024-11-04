import streamlit as st
from streamlit.components.v1 import html

def load_css():
    st.markdown("""
    <style>
    .stApp {
        background-color: #0D0D0D;
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
    .section-header {
        color: #763DF2;
        font-size: 36px;
        font-weight: bold;
        margin-top: 40px;
        margin-bottom: 20px;
        text-align: center;
    }
    .feature-box {
        background-color: #421E59;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        transition: transform 0.3s ease-in-out;
    }
    .feature-box:hover {
        transform: scale(1.02);
        background-color: #5129A6;
    }
    .feature-title {
        color: #F2DFF2;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .app-button {
        background-color: #5129A6;
        color: #F2DFF2;
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
        background-color: #763DF2;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .intro-statement {
        background-color: #421E59;
        border-radius: 10px;
        padding: 20px;
        margin: 30px 0;
        text-align: center;
        font-size: 20px;
        color: #F2DFF2;
    }
    p {
        color: #F2DFF2;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    load_css()

    # Logo and Title
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.image("logo.png", width=200, use_column_width=True)

    st.markdown("<p class='tagline'>Effortlessly Create Emotion-Driven, Shareable Content</p>", unsafe_allow_html=True)

    # Introduction
    st.markdown("""
    <div class='intro-statement'>
        <h3>Revolutionize content creation by automating the process from text generation to video production.</h3>
        <p>An AI-powered platform that enables users to generate personalized, high-quality content, effortlessly and quickly.</p>
        <h3>✨ Let Your Words Come Alive</h3>
    </div>
    """, unsafe_allow_html=True)

    # Features section
    st.markdown("<h2 class='section-header'>✨ Features</h2>", unsafe_allow_html=True)

    features = [
        {
            "title": "🎨 AI Poetry Generation",
            "description": "Create beautiful poems in multiple styles and languages using our advanced AI technology."
        },
        {
            "title": "🎵 Text to Speech",
            "description": "Convert your poems into natural-sounding speech with multiple voice options."
        },
        {
            "title": "🎬 Video Generation",
            "description": "Generate stunning visual backgrounds that complement your poetry."
        },
        {
            "title": "🎯 Custom Text Videos",
            "description": "Create videos with your own text and choose from various creative options."
        }
    ]

    for feature in features:
        st.markdown(f"""
        <div class='feature-box'>
            <p class='feature-title'>{feature['title']}</p>
            <p>{feature['description']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Main apps
    st.markdown("<h2 class='section-header'>🚀 Get Started</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("<a href='/Pulse_&_Prism' target='_self' class='app-button'>🎥 Poetry Videos</a>", unsafe_allow_html=True)
    with col2:
        st.markdown("<a href='/Generate_videos_with_your_own_text' target='_self' class='app-button'>📹 Custom Videos</a>", unsafe_allow_html=True)
    with col3:
        st.markdown("<a href='/ARIA_Assistant' target='_self' class='app-button'>🤖 ARIA Chat</a>", unsafe_allow_html=True)
    with col4:
        st.markdown("<a href='/About_Us' target='_self' class='app-button'>👤 About Us</a>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center;'>Created with ❤️ by B-TAJI Crew</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Pulse & Prism",
        page_icon="🎥",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            'About': 'Effortlessly Create Emotion-Driven, Shareable Content'
        }
    )
    main()