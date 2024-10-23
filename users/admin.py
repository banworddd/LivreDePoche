from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, ReadingList

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ReadingList)
