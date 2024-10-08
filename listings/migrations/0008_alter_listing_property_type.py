# Generated by Django 5.0.7 on 2024-09-19 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0007_alter_listing_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='property_type',
            field=models.CharField(choices=[('apartment', 'Apartment'), ('house', 'House'), ('studio', 'Studio'), ('villa', 'Villa'), ('mansion', 'Mansion'), ('cottage', 'Cottage'), ('estate', 'Estate'), ('penthouse', 'Penthouse'), ('loft', 'Loft'), ('flat', 'Flat')], max_length=50),
        ),
    ]
