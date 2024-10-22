from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, ReadingList
from books.models import Book

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('')  # Перенаправление на главную страницу после регистрации
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('')  # Перенаправление на главную страницу после входа
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  # Перенаправление на страницу входа после выхода


def reading_list(request, username):
    user = get_object_or_404(CustomUser, username=username)
    reading_list = ReadingList.objects.filter(user=user)
    return render(request, 'users/reading_list.html', {'user': user, 'reading_list': reading_list})

def my_reading_list(request):
    if request.user.is_authenticated:
        user = request.user
        reading_list = ReadingList.objects.filter(user=user)
        return render(request, 'users/reading_list.html', {'user': user, 'reading_list': reading_list})
    else:
        return redirect('login')  # Перенаправление на страницу логина, если пользователь не аутентифицирован