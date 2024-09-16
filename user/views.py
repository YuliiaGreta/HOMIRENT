from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from listings.models import Listing
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from booking.models import Booking
from django.db.models import Q

User = get_user_model()

# Регистрация
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user:homepage')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})


def homepage(request):
    return render(request, 'user/home.html')

def user_homepage(request, user_id):
    user = get_object_or_404(User, id=user_id)
    bookings = Booking.objects.filter(user=user)  # Получение бронирований пользователя
    return render(request, 'user/homepage.html', {'user': user, 'bookings': bookings})

def user_logout(request):
    logout(request)
    return redirect('user:login')


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user:homepage')
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})


def view_listings(request):
    listings = Listing.objects.all()
    return render(request, 'user/all_listings.html', {'listings': listings})


class ListingListView(ListView):
    model = Listing
    template_name = 'user/all_listings.html'
    context_object_name = 'listings'

    def get_queryset(self):
        queryset = Listing.objects.all()

        # Получение параметров фильтрации
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        location = self.request.GET.get('location')
        rooms = self.request.GET.get('rooms')
        property_type = self.request.GET.get('property_type')
        sort_by = self.request.GET.get('sort_by', 'title')  # Сортировка по умолчанию по названию
        order = self.request.GET.get('order', 'asc')  # По умолчанию по возрастанию

        # Фильтрация по цене
        if min_price:
            try:
                min_price = float(min_price)
                queryset = queryset.filter(price__gte=min_price)
            except ValueError:
                print("Invalid min_price value")

        if max_price:
            try:
                max_price = float(max_price)
                queryset = queryset.filter(price__lte=max_price)
            except ValueError:
                print("Invalid max_price value")

        # Фильтрация по местоположению
        if location:
            queryset = queryset.filter(location__icontains=location)

        # Фильтрация по количеству комнат
        if rooms:
            queryset = queryset.filter(rooms__gte=rooms)

        # Фильтрация по типу жилья
        if property_type:
            queryset = queryset.filter(property_type__icontains=property_type)

        # Сортировка
        if sort_by in ['title', 'price', 'created_at']:
            if order == 'asc':
                queryset = queryset.order_by(sort_by)
            else:
                queryset = queryset.order_by(f'-{sort_by}')

        return queryset
