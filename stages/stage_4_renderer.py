import requests
import json
from config import CREATOMATE_API_KEY

def render_video_from_source(scenes: list, title: str) -> dict:
    """
    Renders the final video by sending a self-contained video script to the Creatomate API,
    bypassing the need for a pre-made template.
    """
    print("--- Stage 4: Renderer (Source Method) ---")
    print("Building a self-contained video payload...")

    url = "https://api.creatomate.com/v1/renders"
    
    headers = {
        'Authorization': f'Bearer {CREATOMATE_API_KEY}',
        'Content-Type': 'application/json',
    }

    # -- Building the timeline --
    # We will construct a timeline of scenes, each with a video, audio, and text element.
    timeline_elements = []
    for scene in scenes:
        scene_composition = {
            "type": "composition",
            "track": 1, # Place each scene on the same track to play sequentially
            "elements": [
                {
                    "type": "video",
                    "source": scene["video_url"],
                    "fit": "cover", # Ensures the video fills the 9:16 frame
                },
                {
                    "type": "audio",
                    # For testing, we use a public placeholder. In a real app, you would
                    # upload the audio generated in Stage 3 and use that public URL here.
                    "source": "https://cdn.creatomate.com/demo-assets/26076129-9b78-4720-a639-166f74353f43.mp3",
                },
                {
                    "type": "text",
                    "text": scene["narration"],
                    "font_family": "Inter",
                    "font_weight": "700",
                    "font_size": 12,
                    "background_color": "rgba(0, 0, 0, 0.7)",
                    "y": "85%",
                    "width": "90%",
                    "height": "auto",
                    "fill_color": "#ffffff",
                    "horizontal_alignment": "center",
                }
            ]
        }
        timeline_elements.append(scene_composition)

    # This is the main JSON payload. It defines the entire video, not just modifications.
    payload = {
        "source": {
            "output_format": "mp4",
            "width": 1080,
            "height": 1920, # Vertical 9:16 format for Shorts/Reels
            "elements": timeline_elements
        }
    }

    print("Sending self-contained render request to Creatomate...")
    try:
        headers['x-api-sync'] = 'true'
        response = requests.post(url, headers=headers, json=payload, timeout=300)
        response.raise_for_status()

        render_data = response.json()
        
        if render_data and render_data[0].get('status') == 'succeeded':
            final_video_url = render_data[0].get('url')
            print(f"✅ Video rendered successfully!")
            return {"final_video_url": final_video_url}
        else:
            error_message = render_data[0].get('error_message', 'Unknown rendering error.')
            print(f"❌ Video rendering failed: {error_message}")
            return {"error": "Video rendering failed", "details": error_message}

    except requests.exceptions.RequestException as e:
        print(f"❌ Error calling Creatomate API: {e}")
        if e.response:
            print(f"    -> Full Error Response from Server: {e.response.text}")
        return {"error": "Creatomate API request failed", "details": str(e)}
