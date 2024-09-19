import django_filters  # Импортирую библиотеку для создания фильтров
from .models import Listing  # Подключаю модель Listing, с которой будем работать в фильтрах

# Создаю класс для фильтрации объявлений
class ListingFilter(django_filters.FilterSet):
    # Фильтр минимальной цены, чтобы отсеивать объявления, которые дешевле указанной суммы
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    # Фильтр максимальной цены, чтобы находить объявления, которые дешевле или равны указанной сумме
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    # Фильтр минимального количества комнат — удобен для тех, кто ищет более просторное жилье
    rooms_min = django_filters.NumberFilter(field_name='rooms', lookup_expr='gte')
    # Фильтр максимального количества комнат — подходит для поиска компактного жилья
    rooms_max = django_filters.NumberFilter(field_name='rooms', lookup_expr='lte')
    # Фильтр по типу недвижимости — выбираю нужный тип из списка, например, квартира или дом
    property_type = django_filters.ChoiceFilter(field_name='property_type', choices=Listing.PROPERTY_TYPES)
    # Фильтр по местоположению — позволяю выбрать город, чтобы сужать поиск по нужной локации
    location = django_filters.ChoiceFilter(field_name='location', choices=Listing.LOCATION_TYPES)

    # Указываю, какие поля модели можно фильтровать
    class Meta:
        model = Listing  # Указываю, что фильтры работают с моделью Listing
        fields = ['price', 'rooms', 'property_type', 'location']  # Определяю поля, доступные для фильтрации
