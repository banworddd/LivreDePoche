from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages

from .models import CustomUser, ReadingList, CurrentlyReadingList, PlannedReadingList, BookReview
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

    # Проверка, является ли текущий пользователь владельцем страницы
    is_owner = request.user == user

    # Обработка удаления книги
    if request.method == 'POST' and is_owner:
        if 'delete_reading' in request.POST:
            reading_id = request.POST.get('delete_reading')
            if reading_id:
                reading_entry = get_object_or_404(ReadingList, id=reading_id)
                if reading_entry.rating is not None:
                    return render(request, 'users/confirm_delete_review.html', {
                        'reading_entry': reading_entry,
                    })
                else:
                    reading_entry.delete()
                    messages.success(request, "Книга удалена из списка прочитанного.")
                    return redirect('reading_list', username=username)

        elif 'confirm_delete_review' in request.POST:
            reading_id = request.POST.get('confirm_delete_review')
            if reading_id:
                reading_entry = get_object_or_404(ReadingList, id=reading_id)
                review = BookReview.objects.filter(user=user, book=reading_entry.book).first()
                if review:
                    review.delete()
                reading_entry.delete()
                messages.success(request, "Книга и отзыв успешно удалены.")
                return redirect('reading_list', username=username)

        elif 'delete_currently_reading' in request.POST:
            currently_reading_id = request.POST.get('delete_currently_reading')
            if currently_reading_id:
                currently_reading_entry = get_object_or_404(CurrentlyReadingList, id=currently_reading_id)
                currently_reading_entry.delete()
                messages.success(request, "Книга удалена из списка 'Читается сейчас'.")
                return redirect('reading_list', username=username)

        elif 'delete_planned_reading' in request.POST:
            planned_reading_id = request.POST.get('delete_planned_reading')
            if planned_reading_id:
                planned_reading_entry = get_object_or_404(PlannedReadingList, id=planned_reading_id)
                planned_reading_entry.delete()
                messages.success(request, "Книга удалена из списка 'Планируется к прочтению'.")
                return redirect('reading_list', username=username)

    # Прочитанное
    reading_list = user.reading_list.all()
    reading_dict = {}
    for item in reading_list:
        author_name = item.book.authors.first().name if item.book.authors.exists() else 'Неизвестный автор'
        if author_name not in reading_dict:
            reading_dict[author_name] = {}
        reading_dict[author_name][item.book.title] = [item.rating, item.read_date, item.id]

    # Читается сейчас
    currently_reading_list = user.currently_reading_list.all()

    # Планируется к прочтению
    planned_reading_list = user.planned_reading_list.all()

    return render(request, 'users/reading_list.html', {
        'user': user,
        'reading_dict': reading_dict,
        'currently_reading_list': currently_reading_list,
        'planned_reading_list': planned_reading_list,
        'is_owner': is_owner,  # Передаем информацию о владельце
    })