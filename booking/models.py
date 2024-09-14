from django.db import models
from rest_framework.exceptions import ValidationError

from listings.models import Listing
from django.conf import settings

class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings'
    )
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name='bookings'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.listing.title} ({self.start_date} - {self.end_date})'

    def book(self):
        if self.start_date > self.end_date:
            raise ValidationError('Start date must be before end date')

        all_booking = Booking.objects.all()
        # if all_booking.exclude(start_date__gt=self.start_date, listing=self.listing):
        #     print(all_booking.exclude(start_date__gt=self.start_date, listing=self.listing))
        #     raise ValidationError('Booking already exists')
        if all_booking.exclude(end_date__lt=self.start_date, start_date__gt=self.end_date, listing=self.listing):
            print(all_booking.exclude(end_date__lt=self.end_date, start_date__gt=self.start_date, listing=self.listing))
            raise ValidationError('Booking already exists')
        #if all_booking:
            #if all_booking.

    def save(self, *args, **kwargs):
        self.book()
        super().save(*args, **kwargs)
