"""
URL configuration for habit_tracking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from habit_app.views import index, register, profile

urlpatterns = [
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/register/', register, name='register'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', index),
    path('admin/', admin.site.urls),
]
