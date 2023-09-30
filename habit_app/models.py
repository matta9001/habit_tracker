from django.db import models
from django.contrib.auth.models import User
from .utils import get_current_utc

import time


def get_default_checkins():
    yesterday_utc = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time() - 86400))
    return [ yesterday_utc ]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile.png')
    habits = models.CharField(max_length=200)
    checkins = models.JSONField(default=get_default_checkins)
