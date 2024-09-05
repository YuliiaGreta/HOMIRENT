from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.exceptions import PermissionDenied

from .models import Listing, Booking  # Импортируем обе модели
from .serializers import ListingSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Listing
from .forms import ListingForm
from .decorators import user_is_landlord

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Listing
from .forms import ListingForm
from .decorators import user_is_landlord

@login_required
@user_is_landlord
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return redirect('create_listing')
    else:
        form = ListingForm()
        return render(request, 'listings/listing_form.html', {'form': form})  # Отображаем форму для создания объявления
    return render(request, 'listings/listing_form.html', {'form': form})

@login_required
@user_is_landlord
def edit_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if listing.owner != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('my_listings')
    else:
        form = ListingForm(instance=listing)
    return render(request, 'listings/listing_form.html', {'form': form})

@login_required
@user_is_landlord
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if listing.owner != request.user:
        raise PermissionDenied
    listing.delete()
    return redirect('my_listings')

@login_required
@user_is_landlord
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'listings/listing_detail.html', {'listing': listing})
@login_required
@user_is_landlord
def view_all_listings(request):
    listings = Listing.objects.all()
    return render(request, 'listings/index.html', {"listings": listings})

@login_required
@user_is_landlord
def view_my_listings(request):
    listings = Listing.objects.filter(owner=request.user)
    for list in listings:
        print(list)
    return render(request, 'listings/my_listings.html', {"listings": listings})





# class ListingViewSet(viewsets.ModelViewSet):
#     queryset = Listing.objects.all()
#     serializer_class = ListingSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['price', 'location', 'rooms', 'property_type']
#     search_fields = ['title', 'description']
#     ordering_fields = ['price', 'created_at']
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#

# class BookingViewSet(viewsets.ModelViewSet):
#     queryset = Booking.objects.all()
#     serializer_class = BookingSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

