from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.exceptions import ValidationError
from .models import Booking
from .forms import BookingForm
from listings.models import Listing
from django.contrib import messages

# Создаю бронирование для конкретного объявления
def create_booking(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)  # Проверяю, что объявление существует
    if request.method == 'POST':
        form = BookingForm(request.POST)  # Получаю данные из формы бронирования
        if form.is_valid():
            booking = form.save(commit=False)  # Создаю объект бронирования, но не сохраняю его пока
            booking.user = request.user  # Устанавливаю текущего пользователя как арендатора
            booking.listing = listing  # Связываю бронирование с объявлением
            try:
                booking.book()  # Проверяю на наличие пересекающихся бронирований
                booking.save()  # Сохраняю бронирование, если нет конфликтов
                messages.success(request, 'Бронирование успешно создано!')  # Показываю сообщение об успехе
                return redirect('booking:booking_list')  # Перенаправляю на список бронирований
            except ValidationError:
                form.add_error(None, "Date error")  # Добавляю ошибку, если есть проблемы с датами
    else:
        form = BookingForm()  # Если запрос не POST, то просто показываю пустую форму

    return render(request, 'booking/create_booking.html', {'form': form, 'listing': listing})  # Показываю форму бронирования

# Отображаю список всех бронирований пользователя
def booking_list(request):
    bookings = Booking.objects.filter()  # Получаю все бронирования, отсортированные по дате начала
    return render(request, 'booking/booking_list.html', {'bookings': bookings})  # Отображаю страницу с бронированиями

# Отмена бронирования
def cancel_booking(request, pk):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, pk=pk)  # Проверяю, что бронирование существует

        if request.user != booking.listing.owner:  # Проверяю, что текущий пользователь — владелец объявления
            messages.error(request, 'У вас нет прав на отмену этого бронирования.')
        booking.status = 'cancelled'  # Меняю статус бронирования на "отменено"
        booking.save()  # Сохраняю изменения
        messages.success(request, 'Бронирование успешно отменено.')  # Сообщаю об успехе
        return redirect('booking:booking_list')  # Перенаправляю на список бронирований

    else:
        messages.error(request, "Неправильный запрос.")  # Вывожу сообщение об ошибке при неверном запросе
        return redirect('booking:cancel_booking', pk=pk)  # Перенаправляю назад

# Отображаю список всех бронирований для арендодателя
def landlord_booking_list(request):
    listings = Listing.objects.filter(owner=request.user)  # Получаю все объявления текущего арендодателя
    bookings = Booking.objects.filter(listing__in=listings).order_by('start_date')  # Получаю бронирования для этих объявлений
    return render(request, 'booking/landlord_booking_list.html', {'bookings': bookings})  # Отображаю бронирования для арендодателя

# Подтверждение бронирования арендодателем
def confirm_booking(request, pk):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, pk=pk)  # Проверяю, что бронирование существует

        if request.user != booking.listing.owner:  # Проверяю, что текущий пользователь — владелец объявления
            messages.error(request, 'У вас нет прав для подтверждения этого бронирования.')

        booking.status = 'confirmed'  # Меняю статус на "подтверждено"
        booking.save()  # Сохраняю изменения

        messages.success(request, 'Бронирование подтверждено.')  # Сообщаю об успешном подтверждении
        return redirect('booking:booking_list')  # Перенаправляю на список бронирований
    else:
        messages.error(request, 'Неправильный запрос.')  # Сообщение об ошибке при неверном методе запроса
        return redirect('booking:confirm_booking', pk=pk)  # Перенаправляю назад
