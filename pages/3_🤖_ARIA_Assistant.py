import streamlit as st
from aria import AriaTextGenerator

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
        margin-bottom: 10px;
    }
    .chat-input {
        background-color: #421E59;
        color: #F2DFF2;
        border: 1px solid #5129A6;
        border-radius: 10px;
        padding: 10px;
    }
    .chat-message {
        background-color: #421E59;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .user-message {
        background-color: #5129A6;
    }
    .assistant-message {
        background-color: #421E59;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    load_css()
    
    st.markdown("<h1 class='main-title'>🤖 ARIA Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p class='tagline'>Your Creative Writing Partner</p>", unsafe_allow_html=True)

    # Initialize ARIA
    if 'aria' not in st.session_state:
        st.session_state.aria = AriaTextGenerator()
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask ARIA anything about poetry or writing..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("ARIA is thinking..."):
                try:
                    response = st.session_state.aria.generate_text(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()