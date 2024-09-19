from django.contrib import admin  # Импортирую модуль admin из Django для регистрации моделей

# Импортирую модель Booking для работы в административной панели
from .models import Booking

# Регистрирую модель бронирования в админке, чтобы можно было управлять бронированиями через панель администратора
admin.site.register(Booking)
