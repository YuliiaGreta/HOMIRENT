from django.db import models
from django.conf import settings  # Импортирую настройки проекта, чтобы использовать модель пользователя

# Модель для представления объявлений
class Listing(models.Model):
    # Я создаю список различных типов недвижимости
    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),  # Квартира
        ('house', 'House'),  # Дом
        ('studio', 'Studio'),  # Студия
        ('villa', 'Villa'),  # Вилла
        ('mansion', 'Mansion'),  # Особняк
        ('cottage', 'Cottage'),  # Коттедж
        ('estate', 'Estate'),  # Поместье
        ('penthouse', 'Penthouse'),  # Пентхаус
        ('loft', 'Loft'),  # Лофт
        ('flat', 'Flat'),  # Квартира
    ]

    # Я создаю список городов Германии, где расположены объекты недвижимости
    LOCATION_TYPES = [
        ('berlin', 'Berlin'),
        ('munich', 'Munich'),
        ('hamburg', 'Hamburg'),
        ('frankfurt', 'Frankfurt'),
        ('cologne', 'Cologne'),
        ('stuttgart', 'Stuttgart'),
        ('düsseldorf', 'Düsseldorf'),
        ('leipzig', 'Leipzig'),
        ('dortmund', 'Dortmund'),
        ('dresden', 'Dresden'),
        ('hannover', 'Hannover'),
        ('bremen', 'Bremen'),
        ('nuremberg', 'Nuremberg'),
        ('essen', 'Essen'),
        ('duisburg', 'Duisburg'),
        ('bochum', 'Bochum'),
        ('wuppertal', 'Wuppertal'),
        ('bielefeld', 'Bielefeld'),
        ('bonn', 'Bonn'),
        ('mannheim', 'Mannheim'),
        ('karlsruhe', 'Karlsruhe'),
        ('augsburg', 'Augsburg'),
        ('wiesbaden', 'Wiesbaden'),
        ('münster', 'Münster'),
        ('gelsenkirchen', 'Gelsenkirchen'),
        ('aachen', 'Aachen'),
        ('braunschweig', 'Braunschweig'),
        ('chemnitz', 'Chemnitz'),
        ('kiel', 'Kiel'),
        ('magdeburg', 'Magdeburg'),
        ('freiburg', 'Freiburg'),
        ('lübeck', 'Lübeck'),
        ('rostock', 'Rostock'),
        ('potsdam', 'Potsdam'),
        ('oberhausen', 'Oberhausen'),
        ('mainz', 'Mainz'),
        ('erfurt', 'Erfurt'),
        ('halle', 'Halle'),
        ('hagen', 'Hagen'),
        ('darmstadt', 'Darmstadt'),
        ('heilbronn', 'Heilbronn'),
        ('kassel', 'Kassel'),
        ('mönchengladbach', 'Mönchengladbach'),
        ('saarbrücken', 'Saarbrücken'),
        ('regensburg', 'Regensburg'),
    ]

    # Поля модели Listing
    title = models.CharField(max_length=255)  # Название объявления
    description = models.TextField()  # Описание объявления
    location = models.CharField(max_length=255, choices=LOCATION_TYPES)  # Местоположение объекта
    price = models.DecimalField(max_digits=10, decimal_places=1)  # Цена объекта недвижимости
    rooms = models.IntegerField()  # Количество комнат
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)  # Тип недвижимости
    status = models.BooleanField(default=True)  # Статус объявления (активно или нет)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)  # Владелец объекта недвижимости
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания объявления
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего обновления объявления

    # Я определяю строковое представление объекта для удобного отображения
    def __str__(self):
        return self.title

# Модель для представления рейтингов и отзывов
class Rating(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)  # Связь с объявлением
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Связь с пользователем, который оставил отзыв
    rating = models.DecimalField(max_digits=2, decimal_places=1)  # Оценка объекта (максимум два знака)
    comment = models.TextField(blank=True, null=True)  # Комментарий к оценке
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания отзыва

    # Уникальное ограничение, чтобы пользователь не мог оставить несколько отзывов для одного объявления
    class Meta:
        unique_together = ('listing', 'user')

    # Строковое представление для удобного отображения
    def __str__(self):
        return f'{self.listing.title} - {self.rating} by {self.user.username}'
