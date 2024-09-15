from django import forms
from .models import Listing, Rating


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'location', 'rooms', 'property_type', 'status']

from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']