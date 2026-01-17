"""
Reusable UI components for the Streamlit app
"""
import streamlit as st
from language_utils import (
    JURISDICTION_MAP, SPECIALTY_MAP, UI_TRANSLATIONS, FOCUS_OPTIONS
)


def render_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
        <style>
        .stChatMessage { border-radius: 10px; padding: 10px; margin-bottom: 10px; }
        .st-emotion-cache-1c7935c { background-color: #f0f2f6; }
        </style>
    """, unsafe_allow_html=True)


def render_language_toggle(current_language):
    """
    Render language toggle buttons
    
    Args:
        current_language (str): Current UI language ('en' or 'el')
    """
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🇬🇧 EN" if current_language == "el" else "🇬🇧 English", 
                     use_container_width=True):
            st.session_state.ui_language = "en"
            st.rerun()
    
    with col2:
        if st.button("🇬🇷 ΕΛ" if current_language == "el" else "🇬🇷 Ελληνικά", 
                     use_container_width=True):
            st.session_state.ui_language = "el"
            st.rerun()


def render_sidebar(is_greek):
    """
    Render the sidebar with settings
    
    Args:
        is_greek (bool): Whether UI is in Greek
        
    Returns:
        dict: Dictionary containing user settings
    """
    with st.sidebar:
        st.title("⚖️ Ρυθμίσεις Νομικού AI" if is_greek else "⚖️ Legal AI Settings")
        
        # Language toggle
        st.markdown("---")
        render_language_toggle(st.session_state.ui_language)
        st.markdown("---")
        
        # Jurisdiction selection
        jurisdiction = st.selectbox(
            UI_TRANSLATIONS["jurisdiction"]["el" if is_greek else "en"],
            ["Greek", "USA (Federal)", "UK", "European Union"],
            format_func=lambda x: JURISDICTION_MAP.get(x, x) if is_greek else x
        )
        
        # Specialty selection
        specialty = st.selectbox(
            UI_TRANSLATIONS["specialty"]["el" if is_greek else "en"],
            ["Criminal Law", "Commercial Law", "Contract Law",
             "Intellectual Property", "Employment Law", "EU Law"],
            format_func=lambda x: SPECIALTY_MAP.get(x, x) if is_greek else x
        )
        
        # File upload
        uploaded_files = st.file_uploader(
            UI_TRANSLATIONS["upload"]["el" if is_greek else "en"],
            type="pdf",
            accept_multiple_files=True
        )
        
        # Advanced options
        with st.expander(UI_TRANSLATIONS["advanced"]["el" if is_greek else "en"]):
            analysis_depth = st.select_slider(
                UI_TRANSLATIONS["depth"]["el" if is_greek else "en"],
                options=["Quick Review", "Standard Analysis", "Deep Dive"],
                value="Standard Analysis"
            )
            
            focus_options = FOCUS_OPTIONS["el" if is_greek else "en"]
            default_focus = focus_options[:2]
            
            focus_area = st.multiselect(
                UI_TRANSLATIONS["focus"]["el" if is_greek else "en"],
                focus_options,
                default=default_focus
            )
        
        # Logout button
        if st.button(UI_TRANSLATIONS["logout"]["el" if is_greek else "en"]):
            st.session_state.logged_in = False
            st.rerun()
    
    return {
        "jurisdiction": jurisdiction,
        "specialty": specialty,
        "uploaded_files": uploaded_files,
        "analysis_depth": analysis_depth,
        "focus_area": focus_area
    }


def render_chat_history(messages):
    """
    Display chat message history
    
    Args:
        messages (list): List of message dictionaries
    """
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def get_chat_placeholder(is_greek):
    """
    Get the chat input placeholder text
    
    Args:
        is_greek (bool): Whether UI is in Greek
        
    Returns:
        str: Placeholder text
    """
    return UI_TRANSLATIONS["placeholder"]["el" if is_greek else "en"]


def get_spinner_text(is_greek):
    """
    Get the loading spinner text
    
    Args:
        is_greek (bool): Whether UI is in Greek
        
    Returns:
        str: Spinner text
    """
    return UI_TRANSLATIONS["analyzing"]["el" if is_greek else "en"]
