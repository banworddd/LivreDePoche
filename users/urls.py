from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'users'
urlpatterns = [

    path ('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),  # Маршрут для логина
    path('logout/', views.user_logout, name='logout'),  # Маршрут для выхода
    path('profile/<str:username>/', views.user_profile, name='profile'),
    path('', views.users_list, name=''),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)