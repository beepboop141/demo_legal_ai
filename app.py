"""
Main Streamlit application 
"""
import streamlit as st
from google.genai import types

from config import APP_TITLE, APP_ICON, PAGE_LAYOUT
from auth import initialize_session_state, login_page, check_authentication
from ui_components import (
    render_custom_css, render_sidebar, render_chat_history,
    get_chat_placeholder, get_spinner_text
)
from language_utils import detect_language
from prompt_builder import build_complete_system_prompt
from ai_service import GeminiService


# Configure Streamlit page
st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout=PAGE_LAYOUT)

# Initialize session state
initialize_session_state()


def main_app():
    """Main application logic"""
    is_greek = st.session_state.ui_language == "el"
    
    # Apply custom CSS
    render_custom_css()
    
    # Render sidebar and get user settings
    settings = render_sidebar(is_greek)
    
    # Main chat interface
    st.title("Draco")
    
    # Display chat history
    render_chat_history(st.session_state.messages)
    
    # Handle user input
    placeholder_text = get_chat_placeholder(is_greek)
    
    if prompt := st.chat_input(placeholder_text):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            spinner_text = get_spinner_text(is_greek)
            
            with st.spinner(spinner_text):
                # Detect language of user prompt
                detected_lang = detect_language(prompt)
                
                # Build system prompt
                system_instruction = build_complete_system_prompt(
                    settings["jurisdiction"],
                    settings["specialty"],
                    settings,
                    detected_lang
                )
                
                # Initialize AI service
                ai_service = GeminiService()
                
                # Build conversation history (excluding current message)
                conversation_contents = ai_service.build_conversation_history(
                    st.session_state.messages[:-1]
                )
                
                # Prepare current message with files
                current_parts = ai_service.prepare_message_with_files(
                    prompt,
                    settings["uploaded_files"]
                )
                
                # Add current message to conversation
                conversation_contents.append({"role": "user", "parts": current_parts})
                
                # Generate response
                response_text = ai_service.generate_response(
                    conversation_contents,
                    system_instruction
                )
                
                # Display and save response
                st.markdown(response_text)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text
                })


# --- MAIN CONTROL FLOW ---
if __name__ == "__main__":
    if not check_authentication():
        login_page()
    else:
        main_app()
