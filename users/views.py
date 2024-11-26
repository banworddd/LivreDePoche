from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect

from .models import CustomUser


def register(request):
    return render(request, 'users/register.html')

def user_login(request):
    return render(request, 'users/login.html')

def user_profile(request, username):
    """Отображает профиль пользователя."""
    profile_user = get_object_or_404(CustomUser, username=username)
    is_owner = request.user.is_authenticated and request.user == profile_user
    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'is_owner': is_owner
    })

def users_list(request):
    return render(request, 'users/users.html')

def user_logout(request):
    logout(request)
    return redirect('index')

