from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .forms import EditUserForm
from .models import UserProfile

import time
from datetime import datetime

def hours_since_time(utc_time_str):
    input_time = datetime.strptime(utc_time_str, '%Y-%m-%d %H:%M:%S')
    current_time = datetime.utcfromtimestamp(time.time())
    time_difference = current_time - input_time
    hours_difference = time_difference.total_seconds() // 3600
    return int(hours_difference)

def index(request):
    return render(request, 'index.html')

@login_required
def profile(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    last_checkin = user_profile.checkins[-1]
    hours_since = hours_since_time(last_checkin)
    checkin_window = min(48 - hours_since, 48)

    context = {}

    if checkin_window >= 48:
        context['border_color'] = 'border-success'
    elif checkin_window >= 24:
        context['border_color'] = 'border-warning'
    elif checkin_window >= 1:
        context['border_color'] = 'border-danger'
    elif checkin_window >= 1:
        context['border_color'] = ''

    if checkin_window >= 48:
        context['window_message'] = f"Good to go!"
    elif checkin_window > 0:
        context['window_message'] = f"You have {checkin_window} hours to check in."

    return render(request, 'profile.html', context)

@login_required
def manage(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = EditUserForm(instance=user_profile)

    return render(request, 'manage.html', {'form': form})