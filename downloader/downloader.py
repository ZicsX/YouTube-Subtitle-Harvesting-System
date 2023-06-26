from youtube_transcript_api import YouTubeTranscriptApi

def download_subtitles(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi'])
        full_transcript = ' ... '.join(entry['text'] for entry in transcript)
        return full_transcript
    except:
        return None
