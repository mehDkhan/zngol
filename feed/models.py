from django.db import models
from account.models import User
from django.utils import timezone


class Post(models.Model):
    STATUS = (('draft','Draft'),('published','Published'))

    author = models.ForeignKey(to=User,
                               on_delete=models.SET_NULL,
                               related_name='feed_posts',
                               null=True
                               )
    title = models.CharField(max_length=140,blank=False,null=False)
    body = models.TextField(max_length=250,blank=False,null=False)
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS, default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=timezone.now())

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.author,self.post)