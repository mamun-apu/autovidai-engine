import requests
import os
import re

# Import the API keys from our central config file
from config import PEXELS_API_KEY, ELEVENLABS_API_KEY

def get_visual_for_scene(visual_prompt: str) -> dict:
    """
    Finds a relevant stock video for a scene's visual description using Pexels.
    """
    print(f"  - Searching for video: '{visual_prompt}'")

    
    # Sanitize the prompt for a better search query
    query = re.sub(r'[^\w\s-]', '', visual_prompt).strip()
    
    if not query:
        print("    -> ⚠️ Visual prompt was empty after sanitization.")
        return {"error": "Empty visual prompt"}

    try:
        headers = {"Authorization": PEXELS_API_KEY}
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=1&orientation=portrait"
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        if data['videos']:
            # Find the best quality vertical video link
            video_files = data['videos'][0]['video_files']
            # Prefer full HD (1080x1920) if available
            vertical_video = next((f for f in video_files if f['width'] == 1080 and f['height'] == 1920), None)
            if not vertical_video:
                # Fallback to the first available video link if no perfect match
                vertical_video = video_files[0]
            
            print(f"    -> ✅ Found video: {vertical_video['link']}")
            return {"video_url": vertical_video['link']}
        else:
            print("    -> ⚠️ No video found on Pexels for this query.")
            return {"error": "No video found"}
            
    except Exception as e:
        print(f"    -> ❌ Pexels API Error: {e}")
        return {"error": "Pexels API request failed"}

def get_audio_for_scene(narration_text: str, scene_index: int) -> dict:
    """
    Generates a voiceover for a scene's narration using ElevenLabs and saves it to a file.
    """
    print(f"  - Generating audio for: '{narration_text}'")
    
    # Create the temp directory if it doesn't exist
    os.makedirs('temp', exist_ok=True)
    
    # Define the output file path
    output_path = os.path.join('temp', f'scene_{scene_index+1}_audio.mp3')

    # ElevenLabs API URL for a specific voice
    tts_url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM" # A default voice ID

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }

    data = {
        "text": narration_text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    try:
        response = requests.post(tts_url, json=data, headers=headers)
        response.raise_for_status()

        # Write the audio content to the file
        with open(output_path, 'wb') as f:
            f.write(response.content)
            
        print(f"    -> ✅ Audio saved to: {output_path}")
        return {"audio_path": output_path}
        

    except Exception as e:
        print(f"    -> ❌ ElevenLabs API Error: {e}")
        return {"error": "ElevenLabs API request failed"}