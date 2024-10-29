from django.urls import path

from . import views
from .views import UserRegistration, UserLogin

urlpatterns = [
    path('registerAPI/', UserRegistration.as_view(), name='registerAPI'),
    path ('register/', views.register, name='register'),
    path('loginAPI/', UserLogin.as_view(), name='loginAPI'),
    path('login/', views.user_login, name='login'),  # Маршрут для логина
    path('logout/', views.user_logout, name='logout'),  # Маршрут для выхода
    path('reading_list/<str:username>/', views.reading_list, name='reading_list'),  # Маршрут для списка прочитанного

]
