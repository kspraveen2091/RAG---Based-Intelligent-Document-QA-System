import os
from dotenv import load_dotenv

load_dotenv()

print("YouTube API key loaded:", bool(os.getenv("YOUTUBE_API_KEY")))