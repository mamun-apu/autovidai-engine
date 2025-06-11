import json
from stages.stage_4_renderer import render_video

# This is a sample data structure that mimics the output of Stage 3.
# We will use this to test Stage 4 directly.
DUMMY_SCENE_DATA = [
    {
        "visual": "A person looking at a beautiful sunset.",
        "narration": "This is the first scene of our test video.",
        "video_url": "https://videos.pexels.com/video-files/4434240/4434240-hd_1080_1920_25fps.mp4",
        "audio_path": "temp/scene_1_audio.mp3"
    },
    {
        "visual": "A person writing in a journal.",
        "narration": "This is the second scene, with different visuals and audio.",
        "video_url": "https://videos.pexels.com/video-files/8873104/8873104-hd_1080_1920_25fps.mp4",
        "audio_path": "temp/scene_2_audio.mp3"
    }
]

def run_stage_4_test():
    """
    A special function to test only the Stage 4 renderer.
    """
    print("🚀 Running in Stage 4 Test Mode... 🚀")
    print("Bypassing Stages 1, 2, and 3.")
    print("-" * 50)

    # We use our dummy data instead of calling the other stages.
    scenes_with_assets = DUMMY_SCENE_DATA
    video_title = "Shotstack Test Video"
    
    # Stage 4 - Calling the Shotstack renderer
    render_result = render_video(scenes_with_assets, video_title)
    if "error" in render_result:
        print("❗️ Stage 4 test failed.")
        return
    
    print("\n✅ Stage 4 Test Complete. Video Rendered!")
    print(f"  -> Final Video URL: {render_result['final_video_url']}")
    print("\n🎉 AutoVidAI Pipeline Finished Successfully! 🎉")


if __name__ == "__main__":
    run_stage_4_test()
