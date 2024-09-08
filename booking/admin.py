from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Booking

# Регистрируем модель бронирования в админке
admin.site.register(Booking)
