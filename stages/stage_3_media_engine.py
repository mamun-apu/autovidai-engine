import os
import time
import requests
import json
from config import RUNWAYML_API_KEY

def generate_visual_for_scene(visual_prompt: str, scene_index: int) -> dict:
    """
    Generates an original video clip for a scene by calling the RunwayML REST API directly.
    """
    print(f"  - Generating AI video for: '{visual_prompt}'")

    headers = {
        'Authorization': f'Bearer {RUNWAYML_API_KEY}',
        'Content-Type': 'application/json',
    }

    # --- THIS IS THE FIX ---
    # The payload to submit the text-to-video task. According to the API
    # documentation, the model-specific parameters must be nested inside
    # a 'text_to_video' object.
    payload = {
        "model": "gen2",
        "text_to_video": {
            "prompt_text": visual_prompt,
            "duration": 4,
            "ratio": "9:16"
        }
    }
    # ----------------------

    try:
        # 1. Submit the task to start the video generation
        submit_response = requests.post('https://api.runwayml.com/v1/tasks', headers=headers, json=payload)
        submit_response.raise_for_status()
        task_id = submit_response.json()['id']
        print(f"    -> RunwayML task submitted. Task ID: {task_id}")

        # 2. Poll the API until the video is ready
        print("    -> Waiting for video generation... (this can take a few minutes per scene)")
        while True:
            time.sleep(10)
            status_url = f"https://api.runwayml.com/v1/tasks/{task_id}"
            status_response = requests.get(status_url, headers=headers)
            status_response.raise_for_status()
            
            status_data = status_response.json()
            status = status_data.get('status')
            print(f"      -> Scene {scene_index+1} status: {status}")

            if status == "SUCCEEDED":
                video_url = status_data.get('outputs', {}).get('video_path')
                if video_url:
                    print(f"    -> ✅ Video for scene {scene_index+1} generated successfully: {video_url}")
                    return {"video_url": video_url}
                else:
                    print(f"    -> ❌ RunwayML task succeeded but no video path was found.")
                    return {"error": "RunwayML task succeeded but no video found"}
            
            elif status == "FAILED":
                error_detail = status_data.get('error', {}).get('detail', 'Unknown error.')
                print(f"    -> ❌ RunwayML task failed: {error_detail}")
                return {"error": "RunwayML task failed", "details": error_detail}

    except requests.RequestException as e:
        print(f"    -> ❌ RunwayML API Request Error: {e}")
        if e.response:
            print(f"      -> Response Body: {e.response.text}")
        return {"error": "RunwayML API request failed", "details": str(e)}
    except Exception as e:
        print(f"    -> ❌ An unexpected error occurred: {e}")
        return {"error": "An unexpected error occurred in visual generation", "details": str(e)}
