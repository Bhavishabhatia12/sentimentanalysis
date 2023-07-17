from django.db import models

class Tweet(models.Model):
    tweet_id = models.CharField(max_length=255, unique=True)
    twitter_handle = models.CharField(max_length=255)
    posting_date = models.DateTimeField()
    message = models.TextField()

    def __str__(self):
        return self.tweet_id
