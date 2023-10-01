from django.db import models
from django.contrib.auth.models import User
from .utils import get_current_utc
from PIL import Image

import time


def get_default_checkins():
    yesterday_utc = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time() - 86400))
    return [ yesterday_utc ]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile.png')
    habits = models.CharField(max_length=200)
    checkins = models.JSONField(default=get_default_checkins)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_picture.path)
        width, height = img.size

        new_dimension = min(width, height)

        left = (width - new_dimension)/2
        top = (height - new_dimension)/2
        right = (width + new_dimension)/2
        bottom = (height + new_dimension)/2

        img = img.crop((left, top, right, bottom))
        img = img.resize((512, 512))
        
        img.save(self.profile_picture.path)