from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, filters
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import PermissionDenied
from .models import Listing, Rating # Импортируем обе модели
from .serializers import ListingSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .forms import ListingForm
from .decorators import user_is_landlord
from .forms import RatingForm
from django.contrib import messages

@login_required
@user_is_landlord
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user  # Устанавливаем владельца
            listing.save()
            return redirect('listings:my_listings')
    else:
        form = ListingForm()  # Пустая форма для создания нового объекта
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
            listing = form.save(commit=False)
            listing.status = 'status' in request.POST  # Обрабатываем статус (активно/неактивно)
            listing.save()
            return redirect('listings:my_listings')  # Перенаправляем на страницу с моими объявлениями
    else:
        form = ListingForm(instance=listing)
    return render(request, 'listings/listing_form.html', {'form': form})  # Отображаем форму редактирования


@login_required
@user_is_landlord
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if listing.owner != request.user:
        raise PermissionDenied
    listing.delete()
    return redirect('listings:my_listings')  # Перенаправление на страницу с моими объявлениями


@login_required
@user_is_landlord
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'listings/listing_detail.html', {'listing': listing})  # Отображаем подробности объявления


@login_required
def view_all_listings(request):
    listings = Listing.objects.all()
    return render(request, 'listings/index.html', {"listings": listings})  # Отображаем все объявления


@login_required
@user_is_landlord
def view_my_listings(request):
    listings = Listing.objects.filter(owner=request.user)
    print(list(listings.values()))
    return render(request, 'listings/my_listings.html', {"listings": listings})  # Отображаем мои объявления

@login_required
def add_rating(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    # Проверка, что пользователь бронировал это объявление
    user_bookings = request.user.booking_set.filter(listing=listing)
    if not user_bookings.exists():
        return render(request, 'listings/error.html', {'message': 'Вы должны забронировать это объявление, чтобы оставить отзыв.'})

    # Проверка, оставлял ли пользователь уже отзыв
    existing_rating = Rating.objects.filter(listing=listing, user=request.user).first()
    if existing_rating:
        return render(request, 'listings/error.html', {'message': 'Вы уже оставили отзыв для этого объявления.'})

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.listing = listing
            rating.save()
            return render(request, 'listings/add_rating.html', {'form': form, 'listing': listing, 'message': 'Спасибо за ваш отзыв!'})
    else:
        form = RatingForm()

    return render(request, 'listings/add_rating.html', {'form': form, 'listing': listing})

def home(request):
    return render(request, 'listings/index.html')

@login_required
def listing_reviews(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    reviews = Rating.objects.filter(listing=listing)
    return render(request, 'listings/listing_reviews.html', {'listing': listing, 'reviews': reviews})


@login_required
def toggle_listing_status(request, listing_id):
    # Получаем объявление
    listing = get_object_or_404(Listing, pk=listing_id)

    # Проверяем, является ли пользователь владельцем объявления
    if listing.owner != request.user:
        raise PermissionDenied("Вы не являетесь владельцем этого объявления")

    # Переключаем статус объявления
    listing.status = not listing.status
    listing.save()

    # Добавляем сообщение об успешном изменении статуса
    if listing.status:
        messages.success(request, 'Объявление активировано.')
    else:
        messages.success(request, 'Объявление деактивировано.')

<<<<<<< HEAD
    return redirect('listings:my_listings')  # Перенаправляем пользователя на страницу с его объявлениями
=======
    return redirect('my_listings')  # Перенаправляем пользователя на страницу с его объявлениями
>>>>>>> 621bda8a80e27402bf9741047b8ec1cc22cc0556
