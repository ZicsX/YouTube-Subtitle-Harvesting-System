from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import logging

logger = logging.getLogger(__name__)

class YouTubeSubtitleDownloader:
    def __init__(self):
        pass

    def download_subtitle(self, video_id):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi'])
            # Concatenate all subtitle segments into a single string
            full_transcript = ' ... '.join(entry['text'] for entry in transcript)
            return full_transcript
        except TranscriptsDisabled:
            logger.warning(f"Transcripts are disabled for video ID: {video_id}")
            raise
        except NoTranscriptFound:
            logger.warning(f"No transcript found for video ID: {video_id}")
            raise
        except Exception as e:
            logger.error(f"An error occurred while downloading the subtitle: {str(e)}")
            raise
