from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path('users/', include('api.urls.users_urls')),
    path('books/', include('api.urls.books_urls')),
]