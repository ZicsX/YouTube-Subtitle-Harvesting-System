from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtubeapi.models import APIKey
import logging

logger = logging.getLogger(__name__)


class YouTubeAPI:
    def __init__(self):
        self.youtube = None
        self.update_api_key()

    def update_api_key(self):
        # Fetch the API key from the database
        try:
            api_key = APIKey.objects.last().key
            # Build the YouTube client
            self.youtube = build("youtube", "v3", developerKey=api_key)
        except APIKey.DoesNotExist:
            logger.error("APIKey not found. Please add an API Key to the database.")
            raise
        except Exception as e:
            logger.error(
                f"An error occurred while initializing the YouTube client: {str(e)}"
            )
            raise

    def search_videos(self, query):
        try:
            search_request = self.youtube.search().list(
                q=query,
                part="snippet",  # Include 'snippet' to get video details like title and description
                type="video",
                videoCaption="closedCaption",
                maxResults=50,
            )
            # Executing the search request
            search_results = search_request.execute()

            # Extracting video IDs and the concatenated text
            video_data = [
                (
                    item["id"]["videoId"],
                    (item["snippet"]["title"] + " " + item["snippet"]["description"]).lower(),
                )
                for item in search_results["items"]
            ]

            return video_data
        except HttpError as e:
            logger.error(f"A HttpError occurred while searching for videos: {str(e)}")
            if e.resp.status == 403:  # If the API quota is exhausted
                logger.warning("API quota is exhausted. Please update the API Key.")
            raise
        except Exception as e:
            logger.error(f"An error occurred while searching for videos: {str(e)}")
            raise

    def check_hindi_captions(self, video_id):
        try:
            captions_request = self.youtube.captions().list(
                part="snippet", videoId=video_id
            )
            # Executing the captions request
            captions_results = captions_request.execute()
            # Checking if any of the captions are in Hindi and are manually created
            for caption in captions_results["items"]:
                if (
                    caption["snippet"]["language"] == "hi"
                    and caption["snippet"]["trackKind"] == "standard"
                ):
                    return True
            return False
        except HttpError as e:
            logger.error(
                f"A HttpError occurred while checking for Hindi captions: {str(e)}"
            )
            if e.resp.status == 403:  # If the API quota is exhausted
                logger.warning("API quota is exhausted. Please update the API Key.")
            raise
        except Exception as e:
            logger.error(
                f"An error occurred while checking for Hindi captions: {str(e)}"
            )
            raise
