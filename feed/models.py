from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class Feed(models.Model):
    STATUS = (('draft','Draft'),('published','Published'))

    author = models.ForeignKey(to=get_user_model(),
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