from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer

from .serializers import UserSerializer, LoginSerializer
from .models import CustomUser, ReadingList, CurrentlyReadingList, PlannedReadingList, BookReview


class UserRegistration(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            if serializer.is_valid():
                user = serializer.save()
                login(request, user)
                send_welcome_email(user)
                return Response({"status": "User created", "id": user.id}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Error in UserRegistration API:", e)
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLogin(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        try:
            if serializer.is_valid():
                email = serializer.validated_data['email']
                #password = serializer.validated_data['password']

                user = CustomUser.objects.get(email=email)

                login(request, user)

                return Response({"status": "Login successful"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Error in UserLogin API:", e)
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def register(request):
    return render(request, 'users/register.html')

def send_welcome_email(user):
    subject = 'Добро пожаловать в наш сервис!'
    message = f'Привет, {user.username}! Спасибо за регистрацию.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(subject, message, email_from, recipient_list)

def user_login(request):
    return render(request, 'users/login.html')

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