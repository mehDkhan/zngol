from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    following = models.ManyToManyField('self',
                                       through='Contact',
                                       related_name='followers',
                                       symmetrical=False)


class Profile(models.Model):

    user = models.ForeignKey(to=get_user_model(),on_delete=models.CASCADE,
                             related_name='profile',null=False)
    bio = models.TextField(max_length=200,blank=True)
    date_of_birth = models.DateField(blank=True,null=True)
    # photo = models.ImageField(blank=True,upload_to='avatars')

    def __str__(self):
        return "{}'s Profile".format(self.user.username)


class Contact(models.Model):
    from_user = models.ForeignKey(to=get_user_model(),
                                  on_delete=models.CASCADE,related_name='rel_from_set')
    to_user = models.ForeignKey(to=get_user_model(),
                                on_delete=models.CASCADE,related_name="rel_to_set")
    created = models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.from_user,self.to_user)
