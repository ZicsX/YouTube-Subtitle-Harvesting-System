from __future__ import absolute_import, unicode_literals
from celery import shared_task
from youtube_api.connector import search_youtube_videos, get_random_sentence_from_subtitle
from downloader.downloader import download_subtitles
from harvester.models import Video, Query

@shared_task(bind=True, max_retries=3)
def search_and_download(self, query):
    try:
        video_ids = search_youtube_videos(query)
        for video_id in video_ids:
            subtitle = download_subtitles(video_id)
            if subtitle is not None:  # Make sure we have a subtitle
                video = Video(video_id=video_id, subtitle=subtitle)
                video.save()  # Saving the video and subtitle to the database
                sentence = get_random_sentence_from_subtitle(subtitle)
                new_query = Query(query=sentence)
                new_query.save()  # Saving the new query to the database
    except Exception as exc:
        raise self.retry(exc=exc)
