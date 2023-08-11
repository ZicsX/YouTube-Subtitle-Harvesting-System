import os
import logging
from dotenv import load_dotenv
from django.db import transaction, connection
from django.core.cache import cache
from celery import shared_task, group
from youtubeapi.youtube import YouTubeAPI
from .models import Video, Query, NoSubtitle
from .utils.tag import Tagger
from .utils.cache_utils import get_system_state
from .utils.s3_utils import S3SubtitleManager
from youtubeapi.downloader import YouTubeSubtitleDownloader

load_dotenv()

logger = logging.getLogger(__name__)
s3_manager = S3SubtitleManager(bucket_name=os.environ.get("BUCKET_NAME"))


def get_unvisited_query():
    try:
        with connection.cursor() as cursor:
            with transaction.atomic():
                cursor.execute("""
                    SELECT id, query 
                    FROM HARVESTER_QUERY 
                    WHERE visited = 0 AND ROWNUM = 1 
                    FOR UPDATE NOWAIT
                """)
                row = cursor.fetchone()

                if row is None:
                    return None

                # Update visited 
                cursor.execute("""
                    UPDATE HARVESTER_QUERY 
                    SET visited = 1 
                    WHERE id = %s
                """, [row[0]])

                # Return query
                return row[1]

    except Exception as e:
        return None


def search_videos(query):
    try:
        youtube_api = YouTubeAPI()
        return youtube_api.search_videos(query)
    except Exception as e:
        logger.error(f"Error occurred while searching videos: {e}")
        return []


from django.db.utils import IntegrityError


@shared_task
def download_subtitle_for_video(video_id, text):
    subtitle_downloader = YouTubeSubtitleDownloader()
    tagger = Tagger("category/tags")

    try:
        if s3_manager.subtitle_exists(video_id):
            logger.info(f"Subtitle for video ID {video_id} already exists in S3.")
            return
        
        subtitles = subtitle_downloader.download_subtitle(video_id)
        if subtitles:
            categories = tagger.tag_string(text)
            new_query = tagger.random_sentence(subtitles)
            
            # Upload to S3
            s3_manager.upload_subtitle(video_id, subtitles)

            try:
                Video.objects.create(video_id=video_id, categories=categories)
                Query.objects.create(query=new_query)
            except IntegrityError:
                logger.info(f"Video ID {video_id} already exists in the database.")
        else:
            try:
                NoSubtitle.objects.create(video_id=video_id)
            except IntegrityError:
                logger.info(
                    f"Video ID {video_id} is already marked as NoSubtitle in the database."
                )
    except Exception as e:
        logger.error(f"Error occurred while downloading CC of video ID {video_id}: {e}")


@shared_task(bind=True)
def search_and_download(self):
    # Store the task id in the cache
    cache.set("search_and_download_task_id", self.request.id)

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
    video_data = search_videos(query)

    # Group all video downloading tasks and execute them in parallel.
    group(
        download_subtitle_for_video.s(video_id, text) for video_id, text in video_data
    )()

    # Recursive call for continuous execution
    search_and_download.delay()
