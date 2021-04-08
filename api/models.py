from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']


class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    put_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-put_at']