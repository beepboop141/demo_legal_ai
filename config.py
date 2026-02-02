"""
Configuration settings for Draco Legal AI
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys and Credentials
API_KEY = os.getenv("GEMINI_API_KEY")
APP_PASSWORD = os.getenv("APP_PASSWORD")

# App Settings
APP_TITLE = "Draco Demo"
APP_ICON = "⚖️"
PAGE_LAYOUT = "wide"

# Gemini Model Configuration
GEMINI_MODEL = "gemini-3-flash-preview"
GEMINI_CONFIG = {
    "temperature": 0.3,
    "top_p": 0.95,
    "top_k": 40
}

# Language Detection Threshold
GREEK_DETECTION_THRESHOLD = 0.3
