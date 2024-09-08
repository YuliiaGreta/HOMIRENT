from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking
from .forms import BookingForm
from listings.models import Listing

# Создание бронирования
def create_booking(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.listing = listing
            booking.save()
            return redirect('booking_list')
    else:
        form = BookingForm(initial={'listing': listing})
    return render(request, 'booking/create_booking.html', {'form': form, 'listing': listing})

# Просмотр всех бронирований пользователя
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/booking_list.html', {'bookings': bookings})

# Отмена бронирования
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.delete()
        return redirect('booking_list')
    return render(request, 'booking/cancel_booking.html', {'booking': booking})

# Подтверждение бронирования арендодателем
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, listing__owner=request.user)
    if request.method == 'POST':
        booking.is_confirmed = True
        booking.save()
        return redirect('booking_list')
    return render(request, 'booking/confirm_booking.html', {'booking': booking})