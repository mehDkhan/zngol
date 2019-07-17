from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    name = models.CharField(max_length=255,blank=True)
    picture = models.ImageField(upload_to='profile_pics',blank=True,null=True)
    location = models.CharField(max_length=50,blank=True,null=True)
    bio = models.CharField(max_length=280,blank=True,null=True)
    date_of_birth = models.DateField(null=True)
    following = models.ManyToManyField('self',
                                       through='Contact',
                                       related_name='followers',
                                       symmetrical=False)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('account:details',kwargs={'username':self.username})

    def get_name(self):
        if self.name:
            return self.name
        else:
            return self.username

class Contact(models.Model):
    from_user = models.ForeignKey(to=User,
                                  on_delete=models.CASCADE,related_name='rel_from_set')
    to_user = models.ForeignKey(to=User,
                                on_delete=models.CASCADE,related_name="rel_to_set")
    created = models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.from_user,self.to_user)
