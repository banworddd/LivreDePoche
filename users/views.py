from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Вход пользователя сразу после регистрации
            return redirect('index')  # Перенаправление на главную страницу после регистрации
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Получение пользователя из формы
            login(request, user)
            return redirect('index')  # Перенаправление на главную страницу после входа
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')  # Перенаправление на страницу входа после выхода


def reading_list(request, username):
    user = get_object_or_404(CustomUser, username=username)

    # Прочитанное
    reading_list = user.reading_list.all()
    reading_dict = {}
    for item in reading_list:
        author_name = item.book.authors.first().name if item.book.authors.exists() else 'Неизвестный автор'
        if author_name not in reading_dict:
            reading_dict[author_name] = {}
        reading_dict[author_name][item.book.title] = [item.rating, item.read_date]

    # Читается сейчас
    currently_reading_list = user.currently_reading_list.all()

    # Планируется к прочтению
    planned_reading_list = user.planned_reading_list.all()

    return render(request, 'users/reading_list.html', {
        'user': user,
        'reading_dict': reading_dict,
        'currently_reading_list': currently_reading_list,
        'planned_reading_list': planned_reading_list,
    })

