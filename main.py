import json
from stages.stage_1_idea_engine import generate_video_idea
from stages.stage_2_scriptwriter import generate_video_script
from stages.stage_3_media_engine import get_audio_for_scene, get_visual_for_scene

# This is the main function that will run our entire workflow.
def run_pipeline():
    """
    Orchestrates the entire video creation pipeline from idea to publish.
    """
    print("🚀 Starting AutoVidAI Pipeline...")

    # For now, we'll hardcode the niche. Later, this could come from a UI or database.
    niche = "Stoicism"

    # --- STAGE 1: IDEA ENGINE ---
    # Call the function from our stage_1 module to generate a video idea.
    video_idea = generate_video_idea(niche)

    # If there was an error, stop the pipeline.
    if "error" in video_idea:
        print("❗️ Pipeline stopped due to an error in Stage 1.")
        return

    print("\n✅ Pipeline Stage 1 Complete. Idea received:")
    # print(json.dumps(video_idea, indent=4))
    print("-" * 50)

   # === STAGE 2: SCRIPTWRITER ===
    video_script = generate_video_script(video_idea)
    if "error" in video_script:
        print("❗️ Pipeline stopped due to an error in Stage 2.")
        return

    print("\n✅ Pipeline Stage 2 Complete. Script received:")
    # print(json.dumps(video_script, indent=4))
    print("-" * 50)

    # === STAGE 3: MEDIA ENGINE ===
    print("--- Stage 3: Media Engine ---")
    scenes_with_assets = []
    for i, scene in enumerate(video_script["scenes"]):
        print(f"Processing Scene {i+1}/{len(video_script['scenes'])}...")
        
        # Get visual asset
        visual_asset = get_visual_for_scene(scene["visual"])
        
        # Get audio asset
        audio_asset = get_audio_for_scene(scene["narration"], i)
        
        if "error" in visual_asset or "error" in audio_asset:
            print(f"❗️ Could not process scene {i+1}. Skipping.")
            continue
            
        # Combine the script with the new asset paths
        scene["video_url"] = visual_asset["video_url"]
        scene["audio_path"] = audio_asset["audio_path"]
        scenes_with_assets.append(scene)

    print("\n✅ Pipeline Stage 3 Complete. All assets processed:")
    # Pretty-print the final data structure
    print(json.dumps(scenes_with_assets, indent=4))
    print("-" * 50)



# This block ensures the pipeline runs when you execute the script directly.
if __name__ == "__main__":
    run_pipeline()
    print("hello world!")
