from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import Booking
from .forms import BookingForm
from listings.models import Listing
from django.contrib import messages

# Создание бронирования
def create_booking(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.listing = listing
            try:
                booking.save()
                messages.success(request, 'Бронирование успешно создано!')
                return redirect('booking:booking_list')
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = BookingForm()

    return render(request, './booking/create_booking.html', {'form': form, 'listing': listing})

# Просмотр всех бронирований пользователя
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/booking_list.html', {'bookings': bookings})

# Отмена бронирования
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.user != request.user:
        raise PermissionDenied
    booking.delete()
    return redirect('booking:booking_list')

# Подтверждение бронирования арендодателем
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, listing__owner=request.user)
    if request.method == 'POST':
        booking.is_confirmed = True
        booking.save()
        return redirect('booking:booking_list')
    return render(request, 'booking/confirm_booking.html', {'booking': booking})

