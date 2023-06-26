from django.db import models

class ApiKeys(models.Model):
    key = models.CharField(max_length=100)

class SearchQuery(models.Model):
    query = models.CharField(max_length=1000)

class Subtitle(models.Model):
    video_id = models.CharField(max_length=100)
    subtitle_text = models.TextField()
