from django.db import models

# Create your models here.
class Question(models.Model):
    topic = models.TextField()
    sub_topic = models.TextField()
    video_title = models.TextField()
    question = models.TextField()
    answer = models.TextField()
    sequence_tree = models.TextField()
    topic_terms = models.TextField()

    def __str__(self):
        return f"{self.topic} ({self.sub_topic}) : {self.question}"

class Order(models.Model):
    topic = models.TextField()
    sub_topic = models.TextField()
    video_title = models.TextField()
    order = models.TextField()
    url_api = models.TextField()
    sequence_tree = models.TextField()
    topic_terms = models.TextField()

    def __str__(self):
        return f"{self.topic} ({self.sub_topic}) : {self.order}"

class Video(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=300)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ["-added"]
