from rest_framework import serializers  # Я импортирую библиотеку для работы с сериализаторами
from .models import Listing  # Я импортирую модель Listing, которая будет использоваться в сериализаторе

# Я создаю сериализатор для модели Listing
class ListingSerializer(serializers.ModelSerializer):
    # Этот сериализатор позволяет преобразовать данные модели Listing в формат JSON или другие форматы, чтобы передавать их через API
    class Meta:
        model = Listing  # Указываю, что данный сериализатор будет работать с моделью Listing
        fields = '__all__'  # Включаю все поля модели Listing для сериализации
