from django import forms  # Я импортирую модуль forms для работы с формами
from .models import Listing, Rating  # Импортирую модели Listing и Rating, чтобы работать с ними в формах

# Форма для создания и редактирования объявлений
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing  # Указываю модель, с которой будет работать форма (Listing)
        fields = ['title', 'description', 'price', 'location', 'rooms', 'property_type', 'status']  # Поля, которые будут использоваться в форме
        # Включаю такие поля, как название, описание, цена, местоположение, количество комнат, тип недвижимости и статус

# Форма для добавления рейтингов и отзывов
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating  # Указываю модель, с которой будет работать форма (Rating)
        fields = ['rating', 'comment']  # Поля для оценки и комментария

    # Здесь я добавляю дополнительную проверку, чтобы оценка была в диапазоне от 1 до 5
    rating = forms.IntegerField(min_value=1, max_value=5, label="Rating (1-5)")
