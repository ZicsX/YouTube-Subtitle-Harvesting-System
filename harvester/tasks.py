from __future__ import absolute_import, unicode_literals
from celery import shared_task
from youtube.connector import search_youtube_videos, get_random_sentence_from_subtitle
from youtube.downloader import download_subtitles
from .models import Video, Query

@shared_task(bind=True, max_retries=3)
def search_youtube(self, query):
    try:
        video_ids = search_youtube_videos(query)
        for video_id in video_ids:
            download_and_save_subtitle.delay(video_id)  # Queue a task for each video
    except Exception as exc:
        raise self.retry(exc=exc)

@shared_task(bind=True, max_retries=3)
def download_and_save_subtitle(self, video_id):
    try:
        subtitle = download_subtitles(video_id)
        if subtitle is not None:  # Make sure we have a subtitle
            video = Video(video_id=video_id, subtitle=subtitle)
            video.save()  # Saving the video and subtitle to the database
            sentence = get_random_sentence_from_subtitle(subtitle)
            new_query = Query(query=sentence)
            new_query.save()  # Saving the new query to the database
    except Exception as exc:
        raise self.retry(exc=exc)
