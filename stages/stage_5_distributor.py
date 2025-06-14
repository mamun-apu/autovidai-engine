import os
import pickle
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

CLIENT_SECRETS_FILE = "client_secret.json"
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service():
    """
    Handles OAuth 2.0 authentication and returns an authenticated service object.
    """
    credentials = None
    token_pickle_path = 'token.pickle'

    if os.path.exists(token_pickle_path):
        with open(token_pickle_path, 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)
        
        with open(token_pickle_path, 'wb') as token:
            pickle.dump(credentials, token)

    return build(API_NAME, API_VERSION, credentials=credentials)

def upload_video_to_youtube(video_url: str, title: str, description: str):
    """
    Downloads a video from a URL and uploads it to YouTube.
    """
    print("--- Stage 5: Distributor (YouTube) ---")
    
    # 1. Download the video file from the render URL
    print(f"  -> Downloading rendered video from: {video_url}")
    try:
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        
        local_video_path = os.path.join('temp', 'final_video_for_upload.mp4')
        with open(local_video_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"  -> Video downloaded successfully to: {local_video_path}")
    except requests.RequestException as e:
        print(f"❌ Failed to download video: {e}")
        return

    # 2. Authenticate and get the YouTube service object
    print("  -> Authenticating with Google...")
    try:
        youtube_service = get_authenticated_service()
        print("  -> Authentication successful.")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        if os.path.exists(local_video_path):
            os.remove(local_video_path)
        return

    # 3. Prepare the video for upload
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['AI', 'Automation', 'Python', 'Shorts'],
            'categoryId': '28' # 28 is for "Science & Technology"
        },
        'status': {
            'privacyStatus': 'private', # Use 'public' or 'unlisted' as needed
            'selfDeclaredMadeForKids': False,
        }
    }

    media_file = MediaFileUpload(local_video_path)

    # 4. Execute the upload
    print("  -> Uploading video to YouTube...")
    try:
        response_upload = youtube_service.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media_file
        ).execute()

        video_id = response_upload.get('id')
        print(f"✅ Video uploaded successfully!")
        print(f"  -> YouTube Video ID: {video_id}")
        print(f"  -> Watch it here: https://www.youtube.com/watch?v={video_id}")

    except Exception as e:
        print(f"❌ An error occurred during upload: {e}")
    finally:
        # 5. Clean up the temporary video file
        if os.path.exists(local_video_path):
            os.remove(local_video_path)
            print(f"  -> Cleaned up temporary file: {local_video_path}")

