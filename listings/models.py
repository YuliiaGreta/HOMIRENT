from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
class Listing(models.Model):
    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('studio', 'Studio'),
    ]
    LOCATION_TYPES = [
        ('berlin', 'Berlin'),
        ('munich', 'Munich'),
        ('hamburg', 'Hamburg'),
        ('frankfurt', 'Frankfurt'),
        ('cologne', 'Cologne'),
        ('stuttgart', 'Stuttgart'),
        ('düsseldorf', 'Düsseldorf'),
        ('halle_saale', 'Halle (Saale)'),
        ('leipzig', 'Leipzig'),
        ('dortmund', 'Dortmund')

    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, choices=LOCATION_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    rooms = models.IntegerField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    status = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


