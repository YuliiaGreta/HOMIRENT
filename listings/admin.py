from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Listing, Rating

admin.site.register(Listing)
admin.site.register(Rating)
