from django.contrib import admin  # Я подключаю админку Django, чтобы управлять моделями через интерфейс администратора

# Импортирую модели, которые нужно зарегистрировать в админке
from .models import Listing, Rating

# Регистрирую модель Listing, чтобы можно было управлять объявлениями через админку
admin.site.register(Listing)

# Регистрирую модель Rating, чтобы отзывы и оценки тоже были доступны в админке
admin.site.register(Rating)
