from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

import Rental
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from listings.models import Listing


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

def  view_listings(request):
    listings = Listing.objects.all()
    return render(request, 'user/all_listings.html', {'listings': listings})