import os
from dotenv import load_dotenv

# Load environment variables from the .env file in the project root
load_dotenv()

# Securely fetch the API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if the API key is loaded correctly
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Make sure it's set in your .env file.")