# harvester/tasks.py
from celery import shared_task
from youtubeapi.youtube import YouTubeAPI
from youtubeapi.downloader import YouTubeSubtitleDownloader
from .models import Video, Query
from django.db import IntegrityError
import random

youtube_api = YouTubeAPI()
subtitle_downloader = YouTubeSubtitleDownloader()


@shared_task()
def search_and_download():
    # Fetching a random query
    query = Query.objects.order_by('?').first()
    if query is None:
        print("No query found in the database. Please add queries to start harvesting subtitles.")
        return

    try:
        # Searching for videos using the query
        video_ids = youtube_api.search_videos(query.query)
    except Exception as e:
        print(f"Error occurred while searching videos: {e}")
        return

    for video_id in video_ids:
        # Checking if the video already exists in the database
        video_exists = Video.objects.filter(video_id=video_id).exists()
        if video_exists:
            print(f"Video ID {video_id} already exists in the database.")
            continue

        try:
            # Checking if the video has Hindi captions
            if youtube_api.check_hindi_captions(video_id):
                # Downloading the subtitles
                subtitles = subtitle_downloader.download_subtitle(video_id)
                # Storing the video and its subtitles
                Video.objects.create(video_id=video_id, subtitle=subtitles)

                # Generating a new query using a random sentence from the subtitles
                sentences = subtitles.split(" ... ")
                new_query = random.choice(sentences)
                Query.objects.create(query=new_query)

        except Exception as e:
            print(f"Error occurred while processing video ID {video_id}: {e}")
            continue

    try:
        # Deleting the used query
        query.delete()
    except Exception as e:
        print(f"Error occurred while deleting query: {e}")

