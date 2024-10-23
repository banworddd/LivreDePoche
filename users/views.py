from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, ReadingList, CurrentlyReadingList, PlannedReadingList
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from books.models import Book

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('')  # Перенаправление на главную страницу после регистрации
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('')  # Перенаправление на главную страницу после входа
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  # Перенаправление на страницу входа после выхода

def reading_list(request, username):
    user = get_object_or_404(CustomUser, username=username)
    reading_list = ReadingList.objects.filter(user=user)
    reading_dict = {}
    for item in reading_list:
        author_name = item.book.authors.first().name
        if author_name not in reading_dict:
            reading_dict[author_name] = {}
        reading_dict[author_name][item.book.title] = [item.rating, item.read_date]

    currently_reading_list = CurrentlyReadingList.objects.filter(user=user)
    currently_reading_dict = {}
    for item in currently_reading_list:
        author_name = item.book.authors.first().name
        if author_name not in currently_reading_dict:
            currently_reading_dict[author_name] = []
        currently_reading_dict[author_name].append(item.book.title)

    planned_reading_list = PlannedReadingList.objects.filter(user=user)
    planned_reading_dict = {}
    for item in planned_reading_list:
        author_name = item.book.authors.first().name
        if author_name not in planned_reading_dict:
            planned_reading_dict[author_name] = []
        planned_reading_dict[author_name].append(item.book.title)

    return render(request, 'users/reading_list.html', {'user': user, 'reading_dict': reading_dict, 'currently_reading_dict': currently_reading_dict, 'planned_reading_dict': planned_reading_dict})




"""def reading_list(request, username):
    user = get_object_or_404(CustomUser, username=username)
    reading_list = ReadingList.objects.filter(user=user)
    reading_dict = {}
    for item in reading_list:
        author_name = item.book.authors.first().name
        if author_name not in reading_dict:
            reading_dict[author_name] = {}
        reading_dict[author_name][item.book.title] = [item.rating, item.read_date]
    return render(request, 'users/reading_list.html', {'user': user, 'reading_dict': reading_dict})

def currently_reading_list(request, username):
    user = get_object_or_404(CustomUser, username=username)
    currently_reading_list = CurrentlyReadingList.objects.filter(user=user)
    currently_reading_dict = {}
    for item in currently_reading_list:
        author_name = item.book.authors.first().name
        if author_name not in currently_reading_dict:
            currently_reading_dict[author_name] = []
        currently_reading_dict[author_name].append(item.book.title)
    return render(request, 'users/currently_reading_list.html', {'user': user, 'currently_reading_dict': currently_reading_dict})

def planned_reading_list(request, username):
    user = get_object_or_404(CustomUser, username=username)
    planned_reading_list = PlannedReadingList.objects.filter(user=user)
    planned_reading_dict = {}
    for item in planned_reading_list:
        author_name = item.book.authors.first().name
        if author_name not in planned_reading_dict:
            planned_reading_dict[author_name] = []
        planned_reading_dict[author_name].append(item.book.title)"""