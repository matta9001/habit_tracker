from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .forms import BioForm
from .models import UserProfile

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def profile(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = BioForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = BioForm(instance=user_profile)

    print(form)
    return render(request, 'profile.html', {'form': form})