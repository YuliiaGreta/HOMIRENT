from django import forms  # Импортирую модуль forms из Django для создания форм
from .models import Booking  # Импортирую модель Booking для создания формы на её основе

# Форма для создания бронирования
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking  # Указываю модель, на основе которой будет строиться форма
        fields = ['start_date', 'end_date']  # Определяю, что форма будет включать только поля для выбора дат

# Форма для проверки доступности бронирования
class AvailabilityForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))  # Поле для выбора даты начала бронирования
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))  # Поле для выбора даты окончания бронирования
