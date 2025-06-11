import time
from config import SHOTSTACK_API_KEY, SHOTSTACK_STAGE
from shotstack_sdk.api import edit_api
from shotstack_sdk.model.clip import Clip
from shotstack_sdk.model.track import Track
from shotstack_sdk.model.timeline import Timeline
from shotstack_sdk.model.output import Output
from shotstack_sdk.model.edit import Edit
from shotstack_sdk.model.video_asset import VideoAsset
from shotstack_sdk.model.soundtrack import Soundtrack
from shotstack_sdk.model.title_asset import TitleAsset
import shotstack_sdk

def render_video(scenes: list, title: str) -> dict:
    """
    Renders the final video using the Shotstack API by building a timeline
    from the provided scenes.
    """
    print("--- Stage 4: Renderer (Using Shotstack) ---")

    # Configure the Shotstack SDK host
    configuration = shotstack_sdk.Configuration(host="https://api.shotstack.io/" + SHOTSTACK_STAGE)
    
    with shotstack_sdk.ApiClient(configuration) as api_client:
        # Manually set the x-api-key header for authentication
        api_client.set_default_header('x-api-key', SHOTSTACK_API_KEY)
        
        api_instance = edit_api.EditApi(api_client)

        clips = []
        start_time = 0.0
        
        # This loop now uses the real data from the previous stages
        for scene in scenes:
            # A simple way to estimate scene duration based on narration length
            words_per_second = 2.5
            duration = max(len(scene["narration"].split()) / words_per_second, 3.0) # Min 3s duration

            # Add the Pexels video clip to the timeline
            video_clip = Clip(
                asset=VideoAsset(src=scene["video_url"], volume=1.0),
                start=start_time,
                length=duration
            )
            
            # Add the caption overlay
            caption_asset = TitleAsset(text=scene["narration"], style="subtitle")
            caption_clip = Clip(
                asset=caption_asset,
                start=start_time,
                length=duration
            )

            clips.append(video_clip)
            clips.append(caption_clip)
            
            # Increment the start time for the next scene
            start_time += duration

        # Use a reliable public domain music URL.
        soundtrack = Soundtrack(src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", effect="fadeOut", volume=0.2)
        
        timeline = Timeline(background="#000000", tracks=[Track(clips=clips)], soundtrack=soundtrack)
        output = Output(format="mp4", resolution="1080")
        edit = Edit(timeline=timeline, output=output)

        try:
            print("Sending render request to Shotstack...")
            api_response = api_instance.post_render(edit)
            render_id = api_response['response']['id']
            print(f"Request accepted. Render ID: {render_id}")

            print("Waiting for render to complete... (this may take a minute)")
            while True:
                time.sleep(10)
                status_response = api_instance.get_render(render_id)
                status = status_response['response']['status']
                print(f"  -> Current status: {status}")
                
                if status == 'done':
                    final_video_url = status_response['response']['url']
                    print("✅ Video rendered successfully!")
                    return {"final_video_url": final_video_url}
                elif status in ['failed', 'cancelled']:
                    error_message = status_response['response'].get('error', 'Unknown render failure.')
                    print(f"❌ Video rendering failed: {error_message}")
                    return {"error": "Shotstack rendering failed"}

        except Exception as e:
            print(f"❌ Error calling Shotstack API: {e}")
            return {"error": "Shotstack API request failed", "details": str(e)}
