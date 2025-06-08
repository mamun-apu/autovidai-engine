import json
import requests
import re
from config import GEMINI_API_KEY # Import the key from our config file

# Define the API URL using the imported key
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

def generate_video_idea(niche: str) -> dict:
    """
    Generates a viral video idea for a specific niche using the Gemini AI.
    """
    print("--- Stage 1: Idea Engine ---")
    print(f"Received niche: {niche}")

    # This "master prompt" tells the AI its role and the exact JSON format to return.
    master_prompt = f"""
    You are an expert social media strategist specializing in creating viral short-form videos.
    Your task is to generate a complete video concept based on the niche: {niche}.

    Return your response as a single, minified JSON object with NO markdown formatting.
    The JSON object must have the following structure:
    {{
        "title": "A short, catchy, title-case title for the video.",
        "hook": "A strong, one-sentence opening line to grab the viewer's attention.",
        "description": "A brief description for the social media post, including 3-5 relevant hashtags.",
        "points": [
            "A list of 3 to 5 key points or facts that will be the main content of the video."
        ],
        "cta": "A clear, short call-to-action for the end of the video."
    }}
    """

    print("Generating idea with Gemini AI...")
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": master_prompt}]}]}

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(payload), timeout=60)
        response.raise_for_status()
        
        response_data = response.json()
        # Use a more robust way to find and extract the JSON from the AI's response
        text_content = response_data['candidates'][0]['content']['parts'][0]['text']
        
        # Find the JSON part of the string, even if it has markdown backticks
        json_match = re.search(r'\{.*\}', text_content, re.DOTALL)
        if not json_match:
            raise json.JSONDecodeError("No JSON object found in response", text_content, 0)
            
        json_text = json_match.group(0)
        
        video_idea = json.loads(json_text)
        print("✅ Idea generated successfully.")
        return video_idea

    except requests.exceptions.RequestException as e:
        print(f"❌ Error calling Gemini API: {e}")
        return {"error": "API request failed", "details": str(e)}
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"❌ Error parsing Gemini response: {e}")
        print(f"Raw Response Text: {locals().get('text_content', 'Not available')}")
        return {"error": "Could not parse API response", "details": str(e)}

