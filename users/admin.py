from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ReadingList

class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ReadingList)