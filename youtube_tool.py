import os
import webbrowser

from dotenv import load_dotenv
from googleapiclient.discovery import build
from langchain.tools import tool

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build(
    "youtube",
    "v3",
    developerKey=YOUTUBE_API_KEY
)


@tool
def play_youtube_song(song_name: str) -> str:
    """Search YouTube for a song and open the best matching video in the browser."""

    request = youtube.search().list(
        part="snippet",
        q=song_name,
        type="video",
        maxResults=1
    )

    response = request.execute()

    if not response["items"]:
        return f"Could not find '{song_name}' on YouTube."

    video_id = response["items"][0]["id"]["videoId"]
    title = response["items"][0]["snippet"]["title"]

    url = f"https://www.youtube.com/watch?v={video_id}"

    webbrowser.open(url)

    return f"Playing '{title}' on YouTube."