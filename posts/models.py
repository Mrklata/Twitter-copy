from django.db import models

from users.models import User, Profile


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    title = models.CharField(max_length=40)
    text = models.TextField()
    image = models.ImageField(upload_to='media', verbose_name='Picture')
    rates = models.ManyToManyField('PostRating', blank=True, related_name='rates')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f'Post: "{self.title}" by {self.user}'


class PostRating(models.Model):
    SECTION = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='related_post')
    rate = models.CharField(choices=SECTION, max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating_user')

    class Meta:
        verbose_name = 'Rate'
        verbose_name_plural = 'Rates'
        unique_together = ('post', 'user')

    def __str__(self):
        return f'Post {self.post.title}, rated {self.rate}, by {self.user.username}'
