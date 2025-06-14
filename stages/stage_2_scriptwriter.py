import json
import re
import requests
from config import GEMINI_API_KEY

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

def generate_video_script(video_idea: dict) -> dict:
    """
    Takes a video idea and generates a detailed, scene-by-scene script.
    """
    print("--- Stage 2: Scriptwriter ---")
    print("Received video idea. Generating script...")

    # We use the data from Stage 1 to build a new, more detailed prompt.
    prompt_template = f"""You are an expert short-form video scriptwriter 
    specialized in creating viral, engaging videos optimized for social media (Shorts, Reels, TikTok). 
    Write a complete video script based on the following concept:

    Concept Title: {video_idea['title']}
    Hook: {video_idea['hook']}
    Key Points: {', '.join(video_idea['points'])}
    Call to Action: {video_idea['cta']}

    Instructions:
    1.  Create exactly 5–7 concise, engaging scenes.
    2.  Scene 1 must start strongly with the provided hook.
    3.  The middle scenes must clearly and creatively present each key point.
    4.  The last scene must end energetically with the provided call to action.
    5.  For each scene, provide a 'visual' (a vivid, descriptive prompt for an AI image/video generator) and a 'narration' (engaging voiceover text, max 15 words).
    
    Respond only with a single minified JSON object. The root object should be a dictionary containing a single key "scenes", which is a list of scene objects. Do not include markdown or any other text outside the JSON object.
    """

    headers = {'Content-Type': 'application/json'}
    # It's good practice to enable safety settings
    payload = {
        "contents": [{"parts": [{"text": prompt_template}]}],
        "generationConfig": {
            "response_mime_type": "application/json", # This is a powerful feature!
        }
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(payload), timeout=90)
        response.raise_for_status()

        # With response_mime_type set to application/json, you can often parse directly
        video_script = response.json()['candidates'][0]['content']['parts'][0]['text']
        
        # The response should already be a JSON string, so you can load it
        parsed_script = json.loads(video_script)

        print("✅ Script generated successfully.")
        return parsed_script

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP Error in Stage 2: {http_err}")
        # It's helpful to print the response body to debug API errors
        print(f"Response body: {response.text}")
        return {"error": "Script generation failed", "details": str(http_err)}
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"❌ Error parsing JSON in Stage 2: {e}")
        # Print the raw text that failed to parse
        if 'response' in locals():
            print(f"Raw response text: {response.json()['candidates'][0]['content']['parts'][0]['text']}")
        return {"error": "Script generation failed", "details": f"Failed to parse JSON response: {e}"}
    except Exception as e:
        print(f"❌ An unexpected error occurred in Stage 2: {e}")
        return {"error": "Script generation failed", "details": str(e)}