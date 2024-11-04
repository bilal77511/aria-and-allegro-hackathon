import streamlit as st
import requests
from pathlib import Path

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
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 15px;
    }
    .feature-box:hover {
        transform: scale(1.02);
        background-color: #5129A6;
    }
    .circular-image {
        border-radius: 50%;
        overflow: hidden;
        width: 150px;
        height: 150px;
        margin: 0 auto;
        border: 3px solid #763DF2;
    }
    .circular-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .team-member-name {
        color: #F2DFF2;
        font-size: 20px;
        text-align: center;
        margin-top: 10px;
    }
    .social-links {
        text-align: center;
        margin-top: 10px;
    }
    .social-button {
        background-color: #5129A6;
        color: #F2DFF2;
        padding: 5px 10px;
        border-radius: 5px;
        text-decoration: none;
        margin: 0 5px;
        font-size: 14px;
    }
    .social-button:hover {
        background-color: #763DF2;
    }
    </style>
    """, unsafe_allow_html=True)

def about_page():
    load_css()
    
    
    st.markdown("<h1 class='main-title'>Pulse & Prism</h1>", unsafe_allow_html=True)
    #st.markdown("<p class='tagline'>Transform Your Words into Visual Poetry</p>", unsafe_allow_html=True)

    # Team Members
    st.markdown("<h2 class='section-header'>Meet the B-TAJI Crew</h2>", unsafe_allow_html=True)
    
    team_members = [
        {
            "name": "MUHAMMAD BILAL",
            "github": "bilal77511",
            "linkedin": "muhammad-bilal-a75782280",
            "image": "https://avatars.githubusercontent.com/u/149602572?v=4"
        },
        {
            "name": "TIJANI .S. OLALEKAN",
            "github": "tsolami",
            "linkedin": "sotijani",
            "image": "https://avatars.githubusercontent.com/u/113607787?v=4"
        },
        {
            "name": "MUHAMMAD IBRAHIM QASMI",
            "github": "muhammadibrahim313",
            "linkedin": "muhammad-ibrahim-qasmi-9876a1297",
            "image": "https://avatars.githubusercontent.com/u/147333130?v=4"
        },
        {
            "name": "MUHAMMAD JAWAD",
            "github": "mj-awad17",
            "linkedin": "muhammad-jawad-86507b201",
            "image": "https://avatars.githubusercontent.com/u/77524488?v=4"
        }
    ]

    cols = st.columns(len(team_members))
    for col, member in zip(cols, team_members):
        with col:
            st.markdown(f"""
                <div class='feature-box'>
                    <div class='circular-image'>
                        <img src="{member['image']}" alt="{member['name']}">
                    </div>
                    <div class='team-member-name'>{member['name']}</div>
                    <div class='social-links'>
                        <a href='https://github.com/{member["github"]}' target='_blank' class='social-button'>GitHub</a>
                        <a href='https://linkedin.com/in/{member["linkedin"]}' target='_blank' class='social-button'>LinkedIn</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    about_page()
