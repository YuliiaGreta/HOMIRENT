# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ListingViewSet, BookingViewSet, ListngAll
# from .views import create_listing, edit_listing, delete_listing
#
# router = DefaultRouter()
# router.register(r'listings', ListingViewSet)
# router.register(r'bookings', BookingViewSet)
#
# urlpatterns = [
#     path('',
#          ),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('listings/new/', views.create_listing, name='create_listing'),
    path('listings/<int:pk>/edit/', views.edit_listing, name='edit_listing'),
    path('listings/<int:pk>/delete/', views.delete_listing, name='delete_listing'),
    path('listings/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listings/viewall/', views.view_all_listings, name='viewall'),
    path('listings/my/', views.view_my_listings, name='my_listings'),
]
