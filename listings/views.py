from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, filters
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import PermissionDenied
from .models import Listing, Rating  # Я импортирую модели Listing и Rating для работы с объявлениями и отзывами
from .serializers import ListingSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .forms import ListingForm
from .decorators import user_is_landlord  # Я добавляю декоратор, чтобы убедиться, что действия может выполнять только арендодатель
from .forms import RatingForm
from django.contrib import messages  # Для отображения сообщений пользователю

# Создание нового объявления
@login_required  # Проверяю, что пользователь залогинен
@user_is_landlord  # Декоратор, чтобы убедиться, что это арендодатель
def create_listing(request):
    if request.method == 'POST':  # Если это POST-запрос, значит, пользователь отправляет форму
        form = ListingForm(request.POST)
        if form.is_valid():  # Если форма валидна, я сохраняю новое объявление
            listing = form.save(commit=False)  # Сохраняю данные формы без непосредственного сохранения в базу данных
            listing.owner = request.user  # Устанавливаю владельца объявления (текущего пользователя)
            listing.save()  # Сохраняю объявление в базу данных
            return redirect('listings:my_listings')  # Перенаправляю пользователя на страницу с его объявлениями
    else:
        form = ListingForm()  # Если это GET-запрос, то я показываю пустую форму для создания нового объявления
    return render(request, 'listings/listing_form.html', {'form': form})  # Отображаю страницу с формой для создания объявления

# Редактирование существующего объявления
@login_required
@user_is_landlord
def edit_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)  # Получаю объявление по его первичному ключу (ID)
    if listing.owner != request.user:  # Проверяю, является ли текущий пользователь владельцем объявления
        raise PermissionDenied  # Если нет, выбрасываю исключение
    if request.method == 'POST':  # Если это POST-запрос, значит, пользователь отправляет форму для редактирования
        form = ListingForm(request.POST, instance=listing)  # Передаю текущие данные объявления в форму
        if form.is_valid():  # Если форма валидна, я сохраняю изменения
            listing = form.save(commit=False)
            listing.status = 'status' in request.POST  # Обрабатываю статус объявления (активно/неактивно)
            listing.save()  # Сохраняю изменения
            return redirect('listings:my_listings')  # Перенаправляю на страницу с моими объявлениями
    else:
        form = ListingForm(instance=listing)  # Если это GET-запрос, я показываю форму с текущими данными объявления
    return render(request, 'listings/listing_form.html', {'form': form})  # Отображаю страницу с формой редактирования

# Удаление объявления
@login_required
@user_is_landlord
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)  # Получаю объявление по его ID
    if listing.owner != request.user:  # Проверяю, является ли текущий пользователь владельцем объявления
        raise PermissionDenied  # Если нет, выбрасываю исключение
    listing.delete()  # Удаляю объявление
    messages.success(request, 'Объявление было успешно удалено.')  # Сообщаю пользователю, что объявление удалено
    return redirect('listings:my_listings')  # Перенаправляю на страницу с моими объявлениями

# Просмотр подробностей объявления
@login_required
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)  # Получаю объявление по его ID
    return render(request, 'listings/listing_detail.html', {'listing': listing})  # Отображаю страницу с подробностями объявления

# Просмотр всех объявлений
@login_required
def view_all_listings(request):
    listings = Listing.objects.all()  # Получаю все объявления
    return render(request, 'listings/index.html', {"listings": listings})  # Отображаю страницу со всеми объявлениями

# Просмотр только своих объявлений
@login_required
@user_is_landlord
def view_my_listings(request):
    listings = Listing.objects.filter(owner=request.user)  # Получаю только те объявления, которые принадлежат текущему пользователю
    print(list(listings.values()))  # Вывожу в консоль для отладки
    return render(request, 'listings/my_listings.html', {"listings": listings})  # Отображаю страницу с моими объявлениями

# Добавление рейтинга к объявлению
@login_required
def add_rating(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)  # Получаю объявление по его ID

    # Проверяю, бронировал ли пользователь это объявление
    user_bookings = request.user.booking_set.filter(listing=listing)
    if not user_bookings.exists():  # Если нет бронирований, показываю ошибку
        return render(request, 'listings/error.html', {'message': 'Вы должны забронировать это объявление, чтобы оставить отзыв.'})

    # Проверяю, оставлял ли пользователь уже отзыв
    existing_rating = Rating.objects.filter(listing=listing, user=request.user).first()
    if existing_rating:  # Если отзыв уже существует, показываю ошибку
        return render(request, 'listings/error.html', {'message': 'Вы уже оставили отзыв для этого объявления.'})

    if request.method == 'POST':  # Если это POST-запрос, обрабатываю форму
        form = RatingForm(request.POST)
        if form.is_valid():  # Если форма валидна, сохраняю отзыв
            rating = form.save(commit=False)
            rating.user = request.user  # Привязываю отзыв к пользователю
            rating.listing = listing  # Привязываю отзыв к объявлению
            rating.save()
            return redirect('booking:booking_list')  # Перенаправляю на список бронирований
    else:
        form = RatingForm()  # Если это GET-запрос, показываю пустую форму
    return render(request, 'listings/add_rating.html', {'form': form, 'listing': listing})  # Отображаю форму для добавления рейтинга

# Домашняя страница
def home(request):
    return render(request, 'listings/index.html')  # Отображаю домашнюю страницу

# Просмотр отзывов для конкретного объявления
@login_required
def listing_reviews(request, pk):
    listing = get_object_or_404(Listing, pk=pk)  # Получаю объявление по его ID
    reviews = Rating.objects.filter(listing=listing)  # Получаю все отзывы для этого объявления
    return render(request, 'listings/listing_reviews.html', {'listing': listing, 'reviews': reviews})  # Отображаю страницу с отзывами

# Переключение статуса объявления (активно/неактивно)
@login_required
def toggle_listing_status(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)  # Получаю объявление по его ID

    # Проверяю, является ли пользователь владельцем объявления
    if listing.owner != request.user:
        raise PermissionDenied("Вы не являетесь владельцем этого объявления")  # Если нет, выбрасываю исключение

    # Переключаю статус объявления
    listing.status = not listing.status
    listing.save()

    # Добавляю сообщение о том, что статус успешно изменен
    if listing.status:
        messages.success(request, 'Объявление активировано.')  # Если объявление активировано, показываю это сообщение
    else:
        messages.success(request, 'Объявление деактивировано.')  # Если деактивировано, показываю это сообщение

    return redirect('listings:my_listings')  # Перенаправляю пользователя на страницу с его объявлениями
