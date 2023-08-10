import logging
from harvester.utils.tag import Tagger
from celery import shared_task, group
from youtubeapi.youtube import YouTubeAPI
from youtubeapi.downloader import YouTubeSubtitleDownloader
from .models import Video, Query, NoSubtitle
from .utils.cache_utils import get_system_state
from django.core.cache import cache
from django.db import transaction


logger = logging.getLogger(__name__)
youtube_api = YouTubeAPI()
subtitle_downloader = YouTubeSubtitleDownloader()
tagger = Tagger("category/tags")


@transaction.atomic
def get_unvisited_query():
    query = Query.objects.select_for_update().filter(visited=False).first()

    if query:
        query.visited = True
        query.save()

    return query

def search_videos(query):
    try:
        return youtube_api.search_videos(query)
    except Exception as e:
        logger.error(f"Error occurred while searching videos: {e}")
        return []


from django.db.utils import IntegrityError

@shared_task
def download_subtitle_for_video(video_id, text):
    try:
        subtitles = subtitle_downloader.download_subtitle(video_id)
        if subtitles:
            categories = tagger.tag_string(text)
            new_query = tagger.random_sentence(subtitles)

            try:
                Video.objects.create(video_id=video_id, subtitle=subtitles, categories=categories)
                Query.objects.create(query=new_query)
            except IntegrityError:
                logger.info(f"Video ID {video_id} already exists in the database.")
        else:
            try:
                NoSubtitle.objects.create(video_id=video_id)
            except IntegrityError:
                logger.info(f"Video ID {video_id} is already marked as NoSubtitle in the database.")
    except Exception as e:
        logger.error(f"Error occurred while downloading CC of video ID {video_id}: {e}")


@shared_task(bind=True)
def search_and_download(self):
    # Store the task id in the cache
    cache.set('search_and_download_task_id', self.request.id)

    # Fetch system state
    state = get_system_state()

    if not state.is_running:
        return

    query = get_unvisited_query()

    if query is None:
        logger.warning(
            "No query found in the database. Please add queries to start harvesting subtitles."
        )
        return

    # Searching for videos using the query
    video_data = search_videos(query.query)

    # Group all video downloading tasks and execute them in parallel.
    group(
        download_subtitle_for_video.s(video_id, text) for video_id, text in video_data
    )()

    # Recursive call for continuous execution
    search_and_download.delay()
