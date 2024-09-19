from django.apps import AppConfig


# Я создаю конфигурацию для приложения "user"
class UserConfig(AppConfig):
    # Это поле определяет, какой тип поля автоматически использовать для первичных ключей, если оно не указано явно в моделях
    default_auto_field = 'django.db.models.BigAutoField'

    # Здесь я задаю имя приложения
    name = 'user'
