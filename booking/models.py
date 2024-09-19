from django.db import models  # Импортирую модели Django для создания структур данных
from rest_framework.exceptions import ValidationError  # Импортирую исключение для проверки данных
from django.contrib.auth import get_user_model  # Подключаю функцию для получения модели пользователя
from listings.models import Listing  # Импортирую модель Listing для связи с бронированиями
from django.conf import settings  # Импортирую настройки проекта

User = get_user_model()  # Получаю модель пользователя

class Booking(models.Model):
    # Определяю возможные статусы для бронирований
    CONFIRM_TYPES = [
        ("waiting", "Waiting for confirm"),  # Ожидает подтверждения
        ("confirmed", "Confirmed"),  # Подтверждено
        ("cancelled", "Cancelled")  # Отменено
    ]

    # Поле для связи с объявлением, на которое бронирование
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    # Поле для пользователя, который делает бронирование
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Поля для начала и окончания бронирования
    start_date = models.DateField()
    end_date = models.DateField()

    # Поле для статуса бронирования с выбором из доступных значений и значением по умолчанию
    status = models.CharField(
        max_length=255,
        choices=CONFIRM_TYPES,
        default="waiting"  # Значение по умолчанию — "Ожидает подтверждения"
    )

    # Поле с автоматической записью даты создания бронирования
    created_at = models.DateTimeField(auto_now_add=True)  # Добавляю auto_now_add=True для автоматической записи даты

    # Метод для проверки пересекающихся бронирований
    def book(self):
        overlapping_bookings = Booking.objects.filter(
            listing=self.listing,
            start_date__lt=self.end_date,  # Проверяю, что дата начала бронирования меньше даты окончания другого бронирования
            end_date__gt=self.start_date  # Проверяю, что дата окончания бронирования больше даты начала другого бронирования
        ).exclude(pk=self.pk)  # Исключаю текущее бронирование, если оно уже существует

        if overlapping_bookings.exists():
            raise ValidationError('Booking already exists')  # Выбрасываю ошибку, если пересекающиеся бронирования найдены

    # Переопределяю метод сохранения для добавления проверки перед сохранением
    def save(self, *args, **kwargs):
        self.book()  # Проверка перед сохранением
        super().save(*args, **kwargs)  # Сохраняю запись

class Notification(models.Model):
    # Поле для получателя уведомления (связь с моделью пользователя)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)

    # Поле для объявления, к которому относится уведомление
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    # Текст сообщения уведомления
    message = models.TextField()

    # Поле для автоматической записи даты создания уведомления
    created_at = models.DateTimeField(auto_now_add=True)

    # Поле для отслеживания прочтения уведомления (по умолчанию не прочитано)
    is_read = models.BooleanField(default=False)

    # Метод для удобного отображения объекта уведомления в строковом формате
    def __str__(self):
        return f"Уведомление для {self.recipient.username} о {self.listing.title}"
