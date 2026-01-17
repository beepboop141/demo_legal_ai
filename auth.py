"""
Authentication and login functionality
"""
import streamlit as st
from config import APP_PASSWORD


def initialize_session_state():
    """Initialize session state variables"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if "ui_language" not in st.session_state:
        st.session_state.ui_language = "en"
    
    if "messages" not in st.session_state:
        st.session_state.messages = []


def login_page():
    """Render the login page"""
    is_greek = st.session_state.ui_language == "el"
    
    st.title("🔒 Περιορισμένη Πρόσβαση" if is_greek else "🔒 Restricted Access")
    
    # Language toggle buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇬🇧 English", use_container_width=True):
            st.session_state.ui_language = "en"
            st.rerun()
    with col2:
        if st.button("🇬🇷 Ελληνικά", use_container_width=True):
            st.session_state.ui_language = "el"
            st.rerun()
    
    # Password input
    password = st.text_input(
        "Εισάγετε Κωδικό" if is_greek else "Enter Password",
        type="password"
    )
    
    # Login button
    if st.button("Σύνδεση" if is_greek else "Log In"):
        if password == APP_PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            error_msg = "Λάθος κωδικός. Δεν επιτρέπεται η πρόσβαση." if is_greek else "Incorrect password. Access denied."
            st.error(error_msg)


def check_authentication():
    """
    Check if user is authenticated
    
    Returns:
        bool: True if authenticated, False otherwise
    """
    return st.session_state.get("logged_in", False)
  
