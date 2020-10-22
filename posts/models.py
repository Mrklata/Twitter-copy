from django.db import models

from users.models import User, Profile


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    title = models.CharField(max_length=40)
    text = models.TextField()
    image = models.ImageField(upload_to='media', verbose_name='Picture')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f'Post: "{self.title}" by {self.author}'
