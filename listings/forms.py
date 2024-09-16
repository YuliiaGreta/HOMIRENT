from django import forms
from .models import Listing, Rating


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'location', 'rooms', 'property_type', 'status']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'comment']

    rating = forms.IntegerField(min_value=1, max_value=5, label="Rating (1-5)")