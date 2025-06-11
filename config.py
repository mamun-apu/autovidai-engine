import os
from dotenv import load_dotenv

print("--- Running config.py in FINAL TEST mode ---")
load_dotenv()

# Load working keys from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# --- DIRECTLY PASTE THE CREATOMATE KEY HERE ---
# Replace this placeholder with your actual Creatomate key
CREATOMATE_API_KEY = "fd443587227949eb84142a8a3bbfa828ff39aebf79f6b60207848e18e55bfe0357b8310b8ed8a23b9da04fac93cc0185"

print(f"Using Creatomate Key Starting With: {CREATOMATE_API_KEY[:4]}...")
print("-" * 20)


# --- Safety Validation ---
if "PASTE_YOUR" in CREATOMATE_API_KEY:
    raise ValueError("Please replace the placeholder for CREATOMATE_API_KEY in config.py")
if not PEXELS_API_KEY or not GEMINI_API_KEY or not ELEVENLABS_API_KEY:
    raise ValueError("Could not load Gemini, Pexels, or ElevenLabs key from .env file.")