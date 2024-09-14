from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from listings.models import Listing
from django.views.generic import ListView
from django.db.models import Q

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

        # Пол параметры
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        location = self.request.GET.get('location')
        room_count = self.request.GET.get('room_count')
        property_type = self.request.GET.get('property_type')  # Исправлено название переменной
        sort_by = self.request.GET.get('sort_by', 'created_at')  # По умолчанию сортировка по дате добавления
        order = self.request.GET.get('order', 'asc')  # По умолчанию сортировка по возрастанию

        # Фильтр по параметрам
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if room_count:
            queryset = queryset.filter(room_count__gte=room_count)
        if property_type:
            queryset = queryset.filter(housing_type__icontains=property_type)

        # Сортировка
        if sort_by:
            if order == 'asc':
                queryset = queryset.order_by(sort_by)
            elif order == 'desc':
                queryset = queryset.order_by(f'-{sort_by}')

        return queryset
