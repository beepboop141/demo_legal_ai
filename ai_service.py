"""
AI service layer for handling Gemini API interactions
"""
from google import genai
from google.genai import types
from config import API_KEY, GEMINI_MODEL, GEMINI_CONFIG


class GeminiService:
    """Handles all interactions with Google's Gemini API"""
    
    def __init__(self):
        """Initialize Gemini client"""
        self.client = genai.Client(api_key=API_KEY)
    
    def build_conversation_history(self, messages):
        """
        Convert Streamlit message history to Gemini format
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content'
            
        Returns:
            list: Formatted conversation contents for Gemini
        """
        conversation_contents = []
        
        for msg in messages:
            if msg["role"] == "user":
                conversation_contents.append(
                    types.Content(
                        role="user",
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )
            elif msg["role"] == "assistant":
                conversation_contents.append(
                    types.Content(
                        role="model",
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )
        
        return conversation_contents
    
    def prepare_message_with_files(self, prompt, uploaded_files=None):
        """
        Prepare the current message with optional file attachments
        
        Args:
            prompt (str): User's text prompt
            uploaded_files (list): List of uploaded file objects
            
        Returns:
            list: Message parts including text and files
        """
        current_parts = []
        
        # Add files if present
        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_bytes = uploaded_file.read()
                current_parts.append(
                    types.Part.from_bytes(
                        data=file_bytes,
                        mime_type="application/pdf"
                    )
                )
        
        # Add text prompt
        current_parts.append(types.Part.from_text(text=prompt))
        
        return current_parts
    
    def generate_response(self, conversation_contents, system_instruction):
        """
        Generate a response from Gemini
        
        Args:
            conversation_contents (list): Full conversation history
            system_instruction (str): System prompt for the model
            
        Returns:
            str: Generated response text
        """
        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=conversation_contents,
            config={
                "system_instruction": system_instruction,
                **GEMINI_CONFIG
            }
        )
        
        return response.text
