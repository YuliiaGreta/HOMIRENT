import csv
from django.core.management.base import BaseCommand
from listings.models import Listing
from user.models import User

class Command(BaseCommand):
    help = 'Import listings from CSV file'

    def handle(self, *args, **kwargs):
        with open('CSV', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Пропуск заголовка
            for row in reader:
                title, description, location, price, rooms, property_type, status, owner_id = row
                owner = User.objects.get(id=owner_id)
                listing = Listing(
                    title=title,
                    description=description,
                    location=location,
                    price=price,
                    rooms=rooms,
                    property_type=property_type,
                    status=status,
                    owner=owner
                )
                listing.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully added listing: {title}'))