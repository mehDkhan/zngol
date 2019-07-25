from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    name = models.CharField(max_length=255,blank=True)
    picture = models.ImageField(upload_to='profile_pics/',default='profile_pics/user.png',blank=True,null=True)
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

    def get_followings(self):
        """
        Returns a list of users that are following this user
        """
        ids = Contact.objects.values_list('to_user',flat=True).filter(from_user=self, deleted=False)
        users = User.objects.filter(pk__in=set(ids))
        return users

    def get_followers(self):
        """
        Returns a list of users tha this user is following
        """
        ids = Contact.objects.values_list('from_user',flat=True).filter(to_user=self,deleted=False)
        users = User.objects.filter(pk__in=set(ids))
        return users

    def follow(self,user):
        """
        Self will follow user
        """
        if user not in self.get_followings():
            Contact.objects.create(from_user=self,to_user=user,deleted=False)
            return True
        return False

    def unfollow(self,user):
        """
        Self will un-follow user
        """
        if user in self.get_followings():
            c = Contact.objects.get(from_user=self,to_user=user,deleted=False)
            c.deleted=True
            c.save()
            return True
        return False

    def is_following(self,user):
        """
        Check if self is following user
        """
        return self in user.get_followers()

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
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.from_user,self.to_user)
