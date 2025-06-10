import os
from dotenv import load_dotenv

# Load environment variables from the .env file in the project root
load_dotenv()

# --- Load API Keys ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
CREATOMATE_API_KEY = os.getenv("CREATOMATE_API_KEY")


# --- Validate Core Keys ---
# This is a safety check to ensure the most important keys are present before starting.
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please check your .env file.")

if not PEXELS_API_KEY:
    raise ValueError("PEXELS_API_KEY not found. Please check your .env file.")

if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY not found. Please check your .env file.")

