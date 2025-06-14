import os
import time
from config import RUNWAYML_API_KEY
from runwayml import RunwayML

def generate_visual_for_scene(visual_prompt: str, scene_index: int) -> dict:
    """
    Generates an original video clip for a scene using the RunwayML API.
    """
    print(f"  - Generating AI video for: '{visual_prompt}'")

    try:
        # Configure the RunwayML SDK
        client = RunwayML(runway_api_token=RUNWAYML_API_KEY)

        # Submit the text-to-video generation task
        task = client.text_to_video.create(
            model="gen2", # Use the Gen-2 model
            prompt_text=visual_prompt,
            duration=4, # Generate a 4-second clip
            ratio="9:16" # Vertical format
        )
        task_id = task.id
        print(f"    -> RunwayML task submitted. Task ID: {task_id}")

        # Poll the API until the video is ready
        print("    -> Waiting for video generation...")
        while True:
            # Wait for 10 seconds before checking the status
            time.sleep(10)
            retrieved_task = client.tasks.retrieve(task_id)
            status = retrieved_task.status
            print(f"      -> Current status: {status}")

            if status == "SUCCEEDED":
                video_url = retrieved_task.outputs.video_path
                print(f"    -> ✅ Video generated successfully: {video_url}")
                return {"video_url": video_url}
            elif status == "FAILED":
                print("    -> ❌ RunwayML task failed.")
                return {"error": "RunwayML task failed"}

    except Exception as e:
        print(f"    -> ❌ RunwayML API Error: {e}")
        return {"error": "RunwayML API request failed", "details": str(e)}

# We keep the audio generation function as is
def get_audio_for_scene(narration_text: str, scene_index: int) -> dict:
    # This function remains unchanged from the previous version.
    # It still calls ElevenLabs and saves the audio to the temp/ folder.
    # For brevity, the full code is omitted here, but should be kept in your file.
    print(f"  - Generating audio for: '{narration_text}' (Unchanged)")
    # Simulate success for this example
    output_path = os.path.join('temp', f'scene_{scene_index+1}_audio.mp3')
    return {"audio_path": output_path}
