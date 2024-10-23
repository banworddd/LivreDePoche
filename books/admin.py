from django import forms
from django.contrib import admin
from .models import Author, Book, Genre


# Форма для редактирования автора в админке
class AuthorAdminForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}, format='%d-%m-%Y'),
            'date_of_death': forms.DateInput(attrs={'type': 'date'}, format='%d-%m-%Y'),
        }


# Класс администратора для модели Author
class AuthorAdmin(admin.ModelAdmin):
    form = AuthorAdminForm  # Используем кастомную форму
    list_display = ('name', 'date_of_birth', 'date_of_death')  # Поля для отображения в списке
    search_fields = ('name',)  # Поля для поиска


# Класс администратора для модели Book
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary')  # Поля для отображения в списке
    search_fields = ('title', 'summary')  # Поля для поиска
    filter_horizontal = ('authors',)  # Горизонтальный фильтр для выбора авторов


# Регистрация моделей с использованием кастомных классов администратора
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre)  # Регистрация модели Genre без кастомного администратора
