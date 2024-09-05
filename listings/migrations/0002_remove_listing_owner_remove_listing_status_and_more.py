# Generated by Django 5.1 on 2024-09-03 15:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='status',
        ),
        migrations.AlterField(
            model_name='listing',
            name='location',
            field=models.CharField(choices=[('berlin', 'Berlin'), ('munich', 'Munich'), ('hamburg', 'Hamburg'), ('frankfurt', 'Frankfurt'), ('cologne', 'Cologne'), ('stuttgart', 'Stuttgart'), ('düsseldorf', 'Düsseldorf'), ('halle_saale', 'Halle (Saale)'), ('leipzig', 'Leipzig'), ('dortmund', 'Dortmund')], max_length=255),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.DecimalField(decimal_places=5, max_digits=10),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
