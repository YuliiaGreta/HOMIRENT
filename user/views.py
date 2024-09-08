from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

import Rental
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from listings.models import Listing
from django.views.generic import ListView


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
    logout(request)  # Завершаем сессию пользователя
    return redirect('user:login')  # Перенаправляем на главную страницу после логаута

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user:homepage')  # Перенаправляем на главную страницу после логина
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

def view_listings(request):
    listings = Listing.objects.all()
    return render(request, 'user/all_listings.html', {'listings': listings})

class ListingListView(ListView):
    model = Listing
    template_name = 'user/all_listings.html'
    def get_queryset(self):
        queryset = Listing.objects.all()
        sort_by = self.request.GET.get('sort_by')
        order = self.request.GET.get('order')
        if sort_by and order:
            if order == 'asc':
                queryset = queryset.order_by(sort_by)
            elif order == 'desc':
                queryset = queryset.order_by(f'-{sort_by}')
        return queryset



