from django.db import models

class Video(models.Model):
    video_id = models.CharField(max_length=50, unique=True)
    subtitle = models.TextField()

class Query(models.Model):
    query = models.TextField()
