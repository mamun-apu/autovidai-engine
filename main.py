import json
import os
from stages.stage_1_idea_engine import generate_video_idea
from stages.stage_2_scriptwriter import generate_video_script
from stages.stage_3_media_engine import get_visual_for_scene, get_audio_for_scene
from stages.stage_4_renderer import render_video # Import the new function

def run_pipeline():
    print("🚀 Starting AutoVidAI Pipeline...")
    niche = "Stoicism"

    # === STAGE 1: IDEA ENGINE ===
    video_idea = generate_video_idea(niche)
    if "error" in video_idea: return print("❗️ Pipeline stopped in Stage 1.")
    print("\n✅ Stage 1 Complete.\n" + "-"*50)

    # === STAGE 2: SCRIPTWRITER ===
    video_script = generate_video_script(video_idea)
    if "error" in video_script or not video_script.get("scenes"): return print("❗️ Pipeline stopped in Stage 2.")
    print("\n✅ Stage 2 Complete.\n" + "-"*50)

    # === STAGE 3: MEDIA ENGINE ===
    print("--- Stage 3: Media Engine ---")
    scenes_with_assets = []
    # This loop requires the audio files to be uploaded to a public URL for Creatomate.
    # For now, we will simulate this by keeping the local path for our records,
    # but the renderer would need a public URL in a real application.
    for i, scene in enumerate(video_script["scenes"]):
        visual = get_visual_for_scene(scene["visual"])
        audio = get_audio_for_scene(scene["narration"], i)
        if "error" in visual or "error" in audio:
            print(f"❗️ Could not process assets for scene {i+1}. Skipping.")
            continue
        scene.update(visual)
        scene.update(audio)
        scenes_with_assets.append(scene)
    
    if not scenes_with_assets: return print("❗️ Pipeline stopped in Stage 3. No assets were gathered.")
    print("\n✅ Stage 3 Complete.\n" + "-"*50)


     # === STAGE 4: RENDERER ===
    # This will now be executed.
    render_result = render_video(scenes_with_assets, video_idea.get("title", "Untitled Video"))
    if "error" in render_result: return print("❗️ Pipeline stopped in Stage 4.")
    
    print("\n✅ Stage 4 Complete. Video Rendered!")
    print(f"  -> Final Video URL: {render_result['final_video_url']}")

    print("\n🎉 AutoVidAI Pipeline Finished Successfully! 🎉")

    print("\n🎉 AutoVidAI Pipeline Finished Successfully! 🎉")
    print("All stages before rendering are complete.")


if __name__ == "__main__":
    run_pipeline()