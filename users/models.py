from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_pic = models.URLField(blank=True)

    groups = models.ManyToManyField('auth.Group',blank=True,related_name='users',verbose_name='groups',help_text='The groups this user belongs to'),
    user_permissions = models.ManyToManyField('auth.Permission',blank=True,verbose_name='permissions',help_text='The permissions this user has'),