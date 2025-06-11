import os
from dotenv import load_dotenv

print("--- Running config.py in TEST mode ---")
load_dotenv()

# Load working keys from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")


SHOTSTACK_API_KEY = os.getenv("SHOTSTACK_API_KEY")
SHOTSTACK_STAGE = "v1" # Use 'v1' for production, 'stage' for sandbox

    # Validate that all necessary keys are present
if not all([GEMINI_API_KEY, PEXELS_API_KEY, ELEVENLABS_API_KEY, SHOTSTACK_API_KEY]):
    raise ValueError("One or more API keys are missing. Please check your .env file.")
    