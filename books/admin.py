from django.contrib import admin
from django import forms
from .models import Author, Book, Genre

class AuthorAdminForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}, format='%d-%m-%Y'),
            'date_of_death': forms.DateInput(attrs={'type': 'date'}, format='%d-%m-%Y'),
        }

class AuthorAdmin(admin.ModelAdmin):
    form = AuthorAdminForm
    list_display = ('name', 'date_of_birth', 'date_of_death')
    search_fields = ('name',)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary')
    search_fields = ('title', 'summary')
    filter_horizontal = ('authors',)

# Регистрация моделей с использованием классов администратора
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre)