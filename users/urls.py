from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # Маршрут для регистрации
    path('login/', views.user_login, name='login'),  # Маршрут для логина
    path('logout/', views.user_logout, name='logout'),  # Маршрут для выхода
    path('reading_list/<str:username>/', views.reading_list, name='reading_list'),  # Маршрут для списка прочитанного
]
