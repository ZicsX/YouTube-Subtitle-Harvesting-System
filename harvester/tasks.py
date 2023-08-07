from celery import shared_task
from youtubeapi.youtube import YouTubeAPI
from youtubeapi.downloader import YouTubeSubtitleDownloader
from youtubeapi.utils import Tagger, random_sentence
from .models import Video, Query, NoSubtitle, SystemState
import logging

logger = logging.getLogger(__name__)


@shared_task()
def search_and_download():
    youtube_api = YouTubeAPI()
    subtitle_downloader = YouTubeSubtitleDownloader()
    tagger = Tagger("category/tags")

    while True:
        try:
            # Check the system state
            state = SystemState.objects.first()
            if state is None or not state.is_running:
                break
            query = Query.objects.order_by("?").first()
            if query is None:
                logger.warning(
                    "No query found in the database. Please add queries to start harvesting subtitles."
                )
                return
            try:
                # Searching for videos using the query
                video_data = youtube_api.search_videos(query.query)
                try:
                    # Deleting the used query
                    query.delete()
                except Exception as e:
                    logger.error(f"Error occurred while deleting query: {e}")
            except Exception as e:
                logger.error(f"Error occurred while searching videos: {e}")
                return

            for video_id, text in video_data:
                # Checking if the video already exists in the database
                video_exists = Video.objects.filter(video_id=video_id).exists()
                if video_exists:
                    logger.info(f"Video ID {video_id} already exists in the database.")
                    continue
                try:
                    # Checking and Downloading the subtitles
                    subtitles = subtitle_downloader.download_subtitle(video_id)

                    if subtitles:
                        #Get categories
                        categories = tagger.tag_string(text)
                        # Storing the video_id and its subtitles
                        Video.objects.create(video_id=video_id, subtitle=subtitles, categories=categories)

                        # Generating a new query using a random sentence from the subtitles
                        new_query = random_sentence(subtitles)
                        Query.objects.create(query=new_query)

                    else:
                        NoSubtitle.objects.create(video_id=video_id)

                except Exception as e:
                    logger.error(
                        f"Error occurred while processing video ID {video_id}: {e}"
                    )
                    continue
        except Exception as e:
            # Handle exception
            logger.error(f"Error occurred: {e}")
            break
