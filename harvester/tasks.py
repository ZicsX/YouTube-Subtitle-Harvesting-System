import logging
from youtubeapi.utils import Tagger
from celery import shared_task, group
from youtubeapi.youtube import YouTubeAPI
from youtubeapi.downloader import YouTubeSubtitleDownloader
from .models import Video, Query, NoSubtitle, SystemState


logger = logging.getLogger(__name__)
youtube_api = YouTubeAPI()
subtitle_downloader = YouTubeSubtitleDownloader()
tagger = Tagger("category/tags")


def search_videos(query):
    try:
        return youtube_api.search_videos(query)
    except Exception as e:
        logger.error(f"Error occurred while searching videos: {e}")
        return []


@shared_task
def download_subtitle_for_video(video_id, text):
    # Checking if the video already exists in the database
    video_exists = Video.objects.filter(video_id=video_id).exists()
    if video_exists:
        logger.info(f"Video ID {video_id} already exists in the database.")
        return

    try:
        subtitles = subtitle_downloader.download_subtitle(video_id)
        if subtitles:
            categories = tagger.tag_string(text)
            Video.objects.create(
                video_id=video_id, subtitle=subtitles, categories=categories
            )
            new_query = tagger.random_sentence(subtitles)
            Query.objects.create(query=new_query)
        else:
            NoSubtitle.objects.create(video_id=video_id)
    except Exception as e:
        logger.error(f"Error occurred while downloading CC of video ID {video_id}: {e}")


@shared_task()
def search_and_download():
    # Check the system state
    state = SystemState.objects.first()
    if state is None or not state.is_running:
        return

    query = Query.objects.filter(visited=False).first()

    if query is None:
        logger.warning(
            "No query found in the database. Please add queries to start harvesting subtitles."
        )
        state.is_running = False
        state.save()
        return

    query.visited = True
    query.save()

    # Searching for videos using the query
    video_data = search_videos(query.query)

    # Group all video downloading tasks and execute them in parallel.
    group(
        download_subtitle_for_video.s(video_id, text) for video_id, text in video_data
    )()

    # Recursive call for continuous execution
    search_and_download.delay()
