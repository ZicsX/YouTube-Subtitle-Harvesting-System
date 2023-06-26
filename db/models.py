from django.db import models

class Video(models.Model):
    video_id = models.CharField(max_length=255, primary_key=True)
    subtitle = models.TextField(blank=True, null=True)

class Query(models.Model):
    USED = 'U'
    UNUSED = 'N'
    QUERY_STATUS_CHOICES = [
        (USED, 'Used'),
        (UNUSED, 'Unused'),
    ]

    query_text = models.TextField()
    status = models.CharField(
        max_length=2,
        choices=QUERY_STATUS_CHOICES,
        default=UNUSED,
    )
