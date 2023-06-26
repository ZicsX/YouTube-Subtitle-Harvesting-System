from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = "AIzaSyCvqY5kMeG4lEdvuTLjZ-UaQWiEXyv9gvw"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=50
    ).execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result["id"]["videoId"])

    return videos
