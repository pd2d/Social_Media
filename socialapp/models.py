from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

#creating tag module storing name and weight
class Tag(models.Model):
    name = models.CharField(max_length=100)
    weight = models.IntegerField(default=1)

class Post(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    tags = models.ManyToManyField(Tag)
    created_date = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.title

class PostImage(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='post_images/')

class LikeDislike(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
