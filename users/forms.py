from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)  # Добавьте другие поля, если необходимо

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
