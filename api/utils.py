from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(user):
    subject = 'Добро пожаловать в наш сервис!'
    message = f'Привет, {user.username}! Спасибо за регистрацию.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(subject, message, email_from, recipient_list)