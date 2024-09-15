from django.db import models
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from listings.models import Listing
from django.conf import settings

User = get_user_model()

class Booking(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Добавляем auto_now_add=True

    def book(self):
        # Проверка на наличие пересекающихся бронирований
        overlapping_bookings = Booking.objects.filter(
            listing=self.listing,
            start_date__lt=self.end_date,
            end_date__gt=self.start_date
        ).exists()

        if overlapping_bookings:
            raise ValidationError('Booking already exists')

    def save(self, *args, **kwargs):
        self.book()  # Проверка перед сохранением
        super().save(*args, **kwargs)  # Сохранение записи

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)  # Получатель уведомления (арендодатель)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)  # Объявление, к которому относится уведомление
    message = models.TextField()  # Сообщение уведомления
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания уведомления
    is_read = models.BooleanField(default=False)  # Прочитано или нет

    def __str__(self):
        return f"Уведомление для {self.recipient.username} о {self.listing.title}"