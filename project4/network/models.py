from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=140)
    timestamp = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name="likes")

    def __str__(self):
        return '{author}: {content} ({timestamp})'.format(
            author=self.author,
            message=self.content,
            timestamp=self.timestamp,
        )

    def likes(self):
        # Returns number of likes on post
        return self.liked_by.all().count()

    class Meta:
        # Orders posts by most recent first
        ordering = ['-timestamp']

FOLLOWING = 'yes'
NOT_FOLLOWING = 'no'
FOLLOWINGSTATUS = (
    (FOLLOWING, 'Following'),
    (NOT_FOLLOWING, 'Not Following'),
)

class Relationship(models.Model):
    rel_fromuser = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='rel_from_user')
                                
    rel_touser = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='rel_to_user')

    status = models.CharField(max_length=10, choices=FOLLOWINGSTATUS)

    def __str__(self):
        return f'{self.rel_from_user.username} likes {self.rel_to_user.username}'