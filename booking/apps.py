from django.apps import AppConfig  # Импортирую AppConfig из django.apps для создания конфигурации приложения

# Определяю класс конфигурации приложения "booking"
class BookingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Устанавливаю тип поля для автоматических первичных ключей
    name = 'booking'  # Указываю имя приложения, которое будет использоваться в проекте
