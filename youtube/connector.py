# import nltk
import re
import random
from googleapiclient.discovery import build


api_key = 'AIzaSyBa4RHKGWpNhBqIRCeWK_8MByCRY3Yc8SY'  # Your API key
youtube = build('youtube', 'v3', developerKey=api_key)

def search_youtube_videos(query):
    search_request = youtube.search().list(
        q=query,
        part="id",
        type="video",
        videoCaption="closedCaption",
        maxResults=50
    )
    search_results = search_request.execute()

    video_ids = [item['id']['videoId'] for item in search_results['items']]

    return video_ids

def get_random_sentence_from_subtitle(subtitle):
    subList = [substring for substring in re.split(r"\s*\.\.\.\s*|\n|\xa0", subtitle) if substring]
    return random.choice(subList)