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
    prompt_template = f"""
    You are a professional short-form video scriptwriter.
    Based on the following video concept, write a complete script.

    Concept Title: {video_idea['title']}
    Hook: {video_idea['hook']}
    Key Points: {', '.join(video_idea['points'])}
    Call to Action: {video_idea['cta']}

    Instructions:
    1.  Create a script with 5 to 7 scenes.
    2.  The first scene must be the hook.
    3.  The last scene must be the call to action.
    4.  Each scene needs a "visual" description and a "narration" text.
    5.  The "visual" should be a rich description for an AI image/video generator (e.g., "Cinematic shot of a lone wolf howling at a full moon, dark forest background").
    6.  The "narration" is the voiceover text for that scene. It should be concise and engaging.

    Return your response as a single, minified JSON object with NO markdown formatting.
    The JSON object must have a single key, "scenes", which is an array of scene objects.
    Example:
    {{"scenes":[
        {{"visual":"A dramatic, close-up shot of a Roman centurion's helmet gleaming in the sun.","narration":"{video_idea['hook']}"}},
        {{"visual":"An animated map showing the vastness of the Roman Empire at its peak.","narration":"At its height, the Roman Empire was a sprawling superpower."}},
        {{"visual":"A digital rendering of the Colosseum being flooded with water.","narration":"But did you know the Colosseum could be flooded for epic naval battles?"}}
    ]}}
    """

    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt_template}]}]}

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(payload), timeout=90)
        response.raise_for_status()

        response_data = response.json()
        text_content = response_data['candidates'][0]['content']['parts'][0]['text']
        
        json_match = re.search(r'\{.*\}', text_content, re.DOTALL)
        if not json_match:
            raise json.JSONDecodeError("No JSON object found in response", text_content, 0)
            
        json_text = json_match.group(0)
        
        video_script = json.loads(json_text)
        print("✅ Script generated successfully.")
        return video_script

    except Exception as e:
        print(f"❌ Error in Stage 2: {e}")
        return {"error": "Script generation failed", "details": str(e)}