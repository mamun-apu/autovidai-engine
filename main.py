import json
from stages.stage_1_idea_engine import generate_video_idea
from stages.stage_2_scriptwriter import generate_video_script
from stages.stage_3_media_engine import generate_visual_for_scene
from stages.stage_4_renderer import render_video
from stages.stage_5_distributor import upload_video_to_youtube

def run_pipeline():
    """
    Orchestrates the entire video creation pipeline from idea to publish.
    """
    print("🚀 Starting AutoVidAI Pipeline...")
    niche = "Incredible Animal Camouflage"

    # Stage 1 -> generating idea using gemini
    video_idea = generate_video_idea(niche)
    
    if "error" in video_idea: return print("❗️ Pipeline stopped in Stage 1.")
    print("\n" + "="*50)
    print("              ORIGINAL VIDEO IDEA")
    print("="*50)
    # Use json.dumps for pretty printing the dictionary
    print(json.dumps(video_idea, indent=4))
    print("\n✅ Stage 1 Complete.\n" + "-"*50)


    # Stage 2 -> generating video script
    video_script = generate_video_script(video_idea)
    
    if "error" in video_script or not video_script.get("scenes"): return print("❗️ Pipeline stopped in Stage 2.")

    print("\n" + "="*50)
    print("              GENERATED VIDEO SCRIPT")
    print("="*50)
    # Use json.dumps for pretty printing the dictionary
    print(json.dumps(video_script, indent=4))
    print("\n" + "="*50)

    print("\n✅ Stage 2 Complete.\n" + "-"*50)

 
    # Stage 3 now calls the new RunwayML function for visuals
    print("--- Stage 3: Media Engine (with RunwayML) ---")
    scenes_with_assets = []
    for i, scene in enumerate(video_script["scenes"]):
        print(f"Processing Scene {i+1}/{len(video_script['scenes'])}...")
        
        # Call the new visual generation function
        visual = generate_visual_for_scene(scene["visual"], i)
        
        
        if "error" in visual:
            print(f"❗️ Could not generate visual for scene {i+1}. Skipping.")
            continue
        
        scene.update(visual)
        scenes_with_assets.append(scene)

        # 1. Print the 'scene' dictionary *before* the update
        print(f"  ➡️ Scene BEFORE update: {scene}")
        
        # 2. Print the 'visual' dictionary that will be used for the update
        print(f"  ➡️ Visual data to add: {visual}")
        
        # This is the line in question
        scene.update(visual)
        
        # 3. Print the 'scene' dictionary *after* the update to see the result
        print(f"  ✅ Scene AFTER update:  {scene}")
    
    if not scenes_with_assets: return print("❗️ Pipeline stopped in Stage 3.")
    print("\n✅ Stage 3 Complete.\n" + "-"*50)

    # Stages 4 & 5 call the Shotstack renderer and YouTube uploader
    render_result = render_video(scenes_with_assets, video_idea.get("title", "AI Generated Video"))
    if "error" in render_result: return print("❗️ Pipeline stopped in Stage 4.")
    print("\n✅ Stage 4 Complete.\n" + "-"*50)

    final_video_url = render_result['final_video_url']
    video_title = video_idea.get('title', 'AI Generated Video')
    video_description = video_idea.get('description', 'This video was generated automatically.')
    upload_video_to_youtube(final_video_url, video_title, video_description)

    print("\n🎉 AutoVidAI Full Pipeline Finished Successfully! 🎉")


if __name__ == "__main__":
    run_pipeline()
