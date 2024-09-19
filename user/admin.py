from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Я использую декоратор @admin.register для регистрации модели User в административной панели
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Здесь я указываю, какие поля будут отображаться в списке пользователей в админке
    list_display = (
    'username', 'email', 'role')  # Показываю имя пользователя, его email и роль (арендатор или арендодатель)

    # Поля, по которым можно искать пользователей в административной панели
    search_fields = ('username', 'email')  # Пользователь может искать других пользователей по имени или email

    # Я добавляю фильтр, чтобы можно было отфильтровать пользователей по их роли (арендатор или арендодатель)
    list_filter = ('role',)  # Это удобно, когда нужно быстро отфильтровать арендаторов или арендодателей
