from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .forms import EditUserForm
from .models import UserProfile

import time
from datetime import datetime

# UTC Format: '2023-09-28 14:17:00'
# Calculates the distance in hours from the input and the current time
def hours_since_time(utc_time_str):
    input_time = datetime.strptime(utc_time_str, '%Y-%m-%d %H:%M:%S')
    current_time = datetime.utcfromtimestamp(time.time())
    time_difference = current_time - input_time
    hours_difference = time_difference.total_seconds() / 3600

    return round(hours_difference)


# Calculates the distance in hours from the two inputs
def compare_utc(utc_time_str_past, utc_time_str_future):
    past = datetime.strptime(utc_time_str_past, '%Y-%m-%d %H:%M:%S')
    future = datetime.strptime(utc_time_str_future, '%Y-%m-%d %H:%M:%S')
    time_difference = future - past
    hours_difference = time_difference.total_seconds() / 3600

    return round(hours_difference)


# Function that finds the longest contiguous streak from the most recent checkin
# This is defined as a smaller than 48 hour window between each sequential checkin
def calculate_streak(utc_list):
    if len(utc_list) <= 1:
        return 0

    streak_index = 0
    utc_list_reversed = utc_list[::-1]
    for i in range(len(utc_list_reversed) - 1):
        hours_difference = compare_utc(utc_list_reversed[i+1], utc_list_reversed[i])
        if hours_difference > 0 and hours_difference <= 48:
            streak_index = i+1
        else:
            break
    
    return compare_utc(utc_list_reversed[streak_index], utc_list_reversed[0])


def index(request):
    return render(request, 'index.html')


@login_required
def profile(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    context = {}

    # checkin Availability
    last_checkin = user_profile.checkins[-1]
    hours_since = hours_since_time(last_checkin)
    checkin_window = min(48 - hours_since, 48)

    if checkin_window >= 48:
        context['border_color'] = 'border-success'
    elif checkin_window >= 24:
        context['border_color'] = 'border-warning'
    elif checkin_window >= 1:
        context['border_color'] = 'border-danger'
    elif checkin_window >= 1:
        context['border_color'] = ''
    if checkin_window >= 48:
        context['window_message'] = f"Great work!"
    elif checkin_window > 0:
        context['window_message'] = f"You have {checkin_window} hours to check in."

    #print(calculate_streak(["2023-09-28 18:17:00", "2023-09-29 18:17:00"]))

    # Calculate Streak 
    streak = round(calculate_streak(user_profile.checkins) / 24)
    context['streak'] = streak

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