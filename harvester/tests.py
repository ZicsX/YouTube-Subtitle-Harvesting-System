from django.test import TestCase
from harvester.models import Query, Video
from harvester.tasks import search_youtube, download_and_save_subtitle
import time

class CeleryTasksTestCase(TestCase):

    def setUp(self):
        # Create a test Query and Video object for testing
        Query.objects.create(query='हिंदी समाचार')
        Video.objects.create(video_id='DDfE7bGxIug', subtitle='हिंदी समाचार!!!')

    def test_search_youtube(self):
        query = Query.objects.first().query
        task = search_youtube.apply_async(args=(query,))  # apply_async() dispatches the task to the Celery worker
        while not task.ready():  # Wait until the task has been processed
            time.sleep(1)
        self.assertIsNotNone(task.result)  # The result attribute contains the task's result

    def test_download_and_save_subtitle(self):
        video_id = Video.objects.first().video_id
        task = download_and_save_subtitle.apply_async(args=(video_id,))
        while not task.ready():
            time.sleep(1)
        self.assertIsNotNone(task.result)
