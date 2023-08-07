import logging
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    TranslationLanguageNotAvailable,
)

logger = logging.getLogger(__name__)


class YouTubeSubtitleDownloader:
    def __init__(self):
        pass

    def download_subtitle(self, video_id):
        try:
            transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
            try:
                transcript = transcripts.find_manually_created_transcript(['hi']).fetch()
                full_transcript = " ... ".join(entry["text"] for entry in transcript)
                return full_transcript
            except NoTranscriptFound as e:
                tr = 0
                for transcript in transcripts:
                    data_dict = {data["language_code"]: data for data in transcript.translation_languages}
                    is_present = "hi" in data_dict
                    if is_present:
                        tr  = transcript
                        break
                if tr:
                    try:
                        transcript =  tr.translate('hi').fetch()
                        full_transcript = " ".join(entry["text"] for entry in transcript)
                        return full_transcript
                    except TranslationLanguageNotAvailable:
                        return False
                else:
                    return False
        except TranscriptsDisabled:
            return False
