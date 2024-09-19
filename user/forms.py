from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# Я создаю собственную форму для регистрации пользователя, расширяя стандартную форму UserCreationForm
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # Здесь я указываю, что форма будет работать с моей моделью User
        fields = ('username', 'email', 'role', 'password1', 'password2')  # Я включаю в форму поля для имени пользователя, электронной почты, роли (арендатор или арендодатель) и паролей
