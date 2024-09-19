from django.apps import AppConfig  # Импортирую класс AppConfig, который использую для настройки приложения

# Я создаю конфигурацию для приложения "listings"
class ListingsConfig(AppConfig):
    # Указываю, что в модели будет использоваться поле BigAutoField для автоматической генерации ID
    default_auto_field = 'django.db.models.BigAutoField'
    # Указываю имя приложения, которое будет зарегистрировано в настройках проекта
    name = 'listings'
