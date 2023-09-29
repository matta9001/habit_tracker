from django.db import models
from django.contrib.auth.models import User
from .utils import get_current_utc

def get_default_empty_list():
    utc_time_str = get_current_utc()
    return [ utc_time_str ]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile.png')
    habits = models.CharField(max_length=200)
    checkins = models.JSONField(default=get_default_empty_list)
