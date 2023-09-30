from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse

from .forms import EditUserForm
from .models import UserProfile
from .utils import calculate_streak, compare_utc, hours_since_time, get_current_utc, level_map


def index(request):
    return render(request, 'index.html')


def public_profile(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)

    context = {}

    context['username'] = username

    # checkin Availability
    last_checkin = user_profile.checkins[-1]
    hours_since = hours_since_time(last_checkin)
    checkin_window = 48 - hours_since

    streak = round(calculate_streak(user_profile.checkins) / 24)
    context['streak'] = streak

    # Get Level Emoji
    level = streak // 7 
    level_capped = min(level, 51)
    context['level_emoji'] = level_map[level_capped]

    return render(request, 'public_profile.html', context)


@login_required
def checkin(request):
    # TODO: Can't checkin if more than 48 hours have passed.
    user_profile = get_object_or_404(UserProfile, user=request.user)

    last_checkin = user_profile.checkins[-1]
    hours_since = hours_since_time(last_checkin)

    if hours_since >= 1 and hours_since <= 48:
        utc_time_str = get_current_utc()
        user_profile.checkins.append(utc_time_str)
        user_profile.save()
    else:
        return HttpResponse(status=403)

    return redirect('/profile')


@login_required
def profile(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    context = {}
    context['checkin_button'] = {}

    # checkin Availability
    last_checkin = user_profile.checkins[-1]
    hours_since = hours_since_time(last_checkin)
    checkin_window = 48 - hours_since

    if checkin_window >= 48:
        context['border_color'] = 'border-success'
    elif checkin_window >= 24:
        context['border_color'] = 'border-warning'
    elif checkin_window >= 1:
        context['border_color'] = 'border-danger'
    elif checkin_window >= 1:
        context['border_color'] = ''

    if checkin_window >= 48:
        context['window_message'] = ""
        context['checkin_button']['label'] = 'Checked In'
        context['checkin_button']['color'] = 'outline-primary'
        context['checkin_button']['destination'] = ''
        context['checkin_button']['disabled'] = 'disabled'
    elif checkin_window > 0:
        context['window_message'] = f"You have {checkin_window} hours to check in."
        context['checkin_button']['label'] = 'Check In'
        context['checkin_button']['color'] = 'success'
        context['checkin_button']['destination'] = 'checkin'
        context['checkin_button']['disabled'] = ''
    else:
        context['window_message'] = ""
        context['checkin_button']['label'] = 'Start Streak!'
        context['checkin_button']['color'] = 'primary'
        context['checkin_button']['destination'] = 'purchase'
        context['checkin_button']['disabled'] = ''

    # Calculate Streak 
    streak = round(calculate_streak(user_profile.checkins) / 24)
    context['streak'] = streak

    # Get Level Emoji
    level = streak // 7 
    level_capped = min(level, 51)
    context['level_emoji'] = level_map[level_capped]

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