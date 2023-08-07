from django.db import models


class Video(models.Model):
    video_id = models.CharField(max_length=50, unique=True)
    subtitle = models.TextField()
    categories = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.video_id


class Query(models.Model):
    query = models.TextField()
    visited = models.BooleanField(default=False)

    def __str__(self):
        return self.query


class SystemState(models.Model):
    is_running = models.BooleanField(default=False)


class NoSubtitle(models.Model):
    video_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.video_id
