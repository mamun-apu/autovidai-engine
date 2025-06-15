import requests
import time
from config import RUNWAYML_API_KEY

def generate_visual_for_scene(visual_prompt: str, scene_index: int) -> dict:
    print(f"  - Generating AI video for: '{visual_prompt}'")

    headers = {
        'Authorization': f'Bearer {RUNWAYML_API_KEY}',
        'Content-Type': 'application/json',
    }

    payload = {
        "model": "gen2",
        "input": {
            "prompt_text": visual_prompt,
            "duration": 4,
            "ratio": "9:16"
        }
    }

    try:
        response = requests.post("https://api.runwayml.com/v1/inference", headers=headers, json=payload)
        if response.status_code != 200:
            print(f"    -> ❌ API Error: {response.status_code}, {response.text}")
            return {"error": response.text}

        task = response.json()
        task_id = task["id"]
        print(f"    -> Task ID: {task_id}")

        # Poll for completion
        while True:
            time.sleep(10)
            status_resp = requests.get(f"https://api.runwayml.com/v1/inference/{task_id}", headers=headers)
            status_data = status_resp.json()
            status = status_data.get("status")
            print(f"      -> Scene {scene_index + 1} status: {status}")

            if status == "succeeded":
                video_url = status_data["outputs"]["video"]
                print(f"    -> ✅ Video URL: {video_url}")
                return {"video_url": video_url}
            elif status == "failed":
                error = status_data.get("error", "Unknown error")
                print(f"    -> ❌ Task failed: {error}")
                return {"error": error}

    except Exception as e:
        print(f"    -> ❌ Exception: {e}")
        return {"error": str(e)}
