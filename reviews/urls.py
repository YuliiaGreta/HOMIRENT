from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('add/<int:listing_id>/', views.add_review, name='add_review'),
    path('listing/<int:listing_id>/', views.listing_reviews, name='listing_reviews'),
]

