import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API Key and Password
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
APP_PASSWORD = os.getenv("APP_PASSWORD")  
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="LegalGPT Demo", page_icon="⚖️", layout="wide")

# --- LOGIN LOGIC START ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.title("🔒 Restricted Access")
    password = st.text_input("Enter Password", type="password")
    if st.button("Log In"):
        if password == APP_PASSWORD:
            st.session_state.logged_in = True
            st.rerun()  # Reloads the app to show the main content
        else:
            st.error("Incorrect password. Access denied.")

def main_app():
    # Custom CSS for a "Legal" look
    st.markdown("""
        <style>
        .stChatMessage { border-radius: 10px; padding: 10px; margin-bottom: 10px; }
        .st-emotion-cache-1c7935c { background-color: #f0f2f6; } /* Sidebar color */
        </style>
    """, unsafe_allow_html=True)

    # 2. Sidebar Settings
    with st.sidebar:
        st.title("⚖️ Legal AI Settings")
        jurisdiction = st.selectbox("Jurisdiction", ["USA (Federal)", "UK", "European Union", "Canada"])
        specialty = st.selectbox("Specialty", ["Contract Law", "Intellectual Property", "Employment Law"])
        uploaded_file = st.file_uploader("Upload Legal Document (PDF)", type="pdf")
        
        # Add a logout button
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.rerun()

        st.info("The AI will use these settings to context-ground its answers.")

    # 3. Chat Logic
    st.title("Draco AI")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 4. Handling Input & Model Call
    if prompt := st.chat_input("Ask a question about your document or legal matter..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Build the instructions based on sidebar
            system_instruction = f"You are a legal expert in {jurisdiction} specializing in {specialty}. "
            
            contents = [prompt]
            
            # If a file is uploaded, add it to the prompt context
            if uploaded_file:
                file_bytes = uploaded_file.read()
                contents.insert(0, types.Part.from_bytes(data=file_bytes, mime_type="application/pdf"))
                system_instruction += "Analyze the attached document and answer specifically based on its clauses."

            # Call Gemini
            response = client.models.generate_content(
                model="gemini-2.0-flash", # Updated to 2.0-flash (standard efficient model)
                contents=contents,
                config={"system_instruction": system_instruction}
            )
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- CONTROL FLOW ---
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
