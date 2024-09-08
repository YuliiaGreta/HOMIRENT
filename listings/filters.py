import django_filters
from .models import Listing

class ListingFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    rooms_min = django_filters.NumberFilter(field_name='rooms', lookup_expr='gte')
    rooms_max = django_filters.NumberFilter(field_name='rooms', lookup_expr='lte')
    property_type = django_filters.ChoiceFilter(field_name='property_type', choices=Listing.PROPERTY_TYPES)
    location = django_filters.ChoiceFilter(field_name='location', choices=Listing.LOCATION_TYPES)

    class Meta:
        model = Listing
        fields = ['price', 'rooms', 'property_type', 'location']

