import json
#from stages.stage_1_idea_engine import generate_video_idea

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
    print(json.dumps(video_idea, indent=4))
    print("-" * 50)

    # --- Subsequent stages will be called here ---
    # e.g., video_script = generate_video_script(video_idea)
    # ...and so on.


# This block ensures the pipeline runs when you execute the script directly.
if __name__ == "__main__":
    run_pipeline()