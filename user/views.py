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
from .decorators import redirect_authenticated_user
from django.contrib.auth.decorators import login_required

User = get_user_model()

# Функция для регистрации нового пользователя
# Здесь я предоставляю пользователю форму для регистрации нового аккаунта
@redirect_authenticated_user  # Декоратор, чтобы перенаправлять аутентифицированного пользователя
def register(request):
    # Если пользователь отправила форму регистрации
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Получаю данные из формы
        if form.is_valid():  # Проверяю, что форма заполнена правильно
            user = form.save()  # Сохраняю нового пользователя в базе данных
            login(request, user)  # Вхожу в аккаунт автоматически после регистрации
            return redirect('user:homepage')  # Перенаправляю на домашнюю страницу после успешной регистрации
        else:
            error_message = form.errors.as_text()  # Если есть ошибки, сохраняю их, чтобы показать пользователю
    else:
        form = CustomUserCreationForm()  # Если форма не была отправлена, показываю пустую форму
        error_message = None  # Ошибок пока нет
    return render(request, 'user/register.html', {'form': form, 'error_message': error_message})  # Возвращаю страницу регистрации

# Функция для отображения домашней страницы
# После входа в аккаунт я перенаправляю пользователя сюда
@login_required  # Пользователь должна быть залогинена, чтобы видеть эту страницу
def homepage(request):
    return render(request, 'user/home.html')  # Просто отображаю домашнюю страницу

# Функция для отображения домашней страницы конкретного пользователя
# Я хочу показать информацию о бронированиях конкретного пользователя
def user_homepage(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Получаю пользователя по его ID или возвращаю 404
    bookings = Booking.objects.filter(user=user)  # Получаю все бронирования этого пользователя
    return render(request, 'user/homepage.html', {'user': user, 'bookings': bookings})  # Отображаю домашнюю страницу пользователя с бронированиями

# Функция для выхода из аккаунта
# Если пользователь хочет выйти из системы, она будет перенаправлена сюда
@login_required  # Убедимся, что пользователь залогинена, прежде чем она сможет выйти
def user_logout(request):
    logout(request)  # Выполняю выход пользователя
    return redirect('user:login')  # После выхода перенаправляю на страницу входа

# Функция для входа в аккаунт
# Здесь я проверяю, есть ли пользователь с введенными данными и логиню её
@redirect_authenticated_user  # Если пользователь уже залогинена, она будет перенаправлена
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Получаю данные из формы входа
        if form.is_valid():  # Проверяю правильность введенных данных
            username = form.cleaned_data.get('username')  # Извлекаю имя пользователя
            password = form.cleaned_data.get('password')  # Извлекаю пароль
            user = authenticate(request, username=username, password=password)  # Проверяю, существует ли пользователь
            if user is not None:  # Если пользователь существует
                login(request, user)  # Логиню пользователя
                return redirect('user:homepage')  # Перенаправляю на домашнюю страницу
    else:
        form = AuthenticationForm()  # Если форма не отправлена, показываю пустую форму
    return render(request, 'user/login.html', {'form': form})  # Возвращаю страницу входа

# Функция для отображения всех активных объявлений
# Я хочу показать все активные объявления, чтобы пользователь могла выбрать нужное
@login_required  # Убедимся, что пользователь залогинена
def view_listings(request):
    listings = Listing.objects.filter(status=True)  # Фильтрую только активные объявления
    return render(request, 'user/all_listings.html', {'listings': listings})  # Отображаю страницу со всеми объявлениями

# Класс для отображения списка объявлений с возможностью фильтрации
# Я хочу, чтобы пользователь могла искать жильё по своим предпочтениям
class ListingListView(ListView):
    model = Listing
    template_name = 'user/all_listings.html'
    context_object_name = 'listings'

    # Метод для получения списка объявлений с учетом фильтров
    def get_queryset(self):
        queryset = Listing.objects.filter(status=True)  # Показываю только активные объявления

        # Получение параметров фильтрации из запроса
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        location = self.request.GET.get('location')
        rooms = self.request.GET.get('rooms')
        property_type = self.request.GET.get('property_type')
        sort_by = self.request.GET.get('sort_by', 'title')  # По умолчанию сортирую по названию
        order = self.request.GET.get('order', 'asc')  # По умолчанию сортировка по возрастанию

        # Фильтрация по минимальной цене
        if min_price:
            try:
                min_price = float(min_price)  # Преобразую значение в число
                queryset = queryset.filter(price__gte=min_price)  # Фильтрую объявления с ценой не ниже указанной
            except ValueError:
                print("Invalid min_price value")  # Если цена некорректна, вывожу сообщение

        # Фильтрация по максимальной цене
        if max_price:
            try:
                max_price = float(max_price)
                queryset = queryset.filter(price__lte=max_price)
            except ValueError:
                print("Invalid max_price value")

        # Фильтрация по местоположению
        if location:
            queryset = queryset.filter(location__icontains=location)  # Фильтрую по введенному местоположению

        # Фильтрация по количеству комнат
        if rooms:
            queryset = queryset.filter(rooms__gte=rooms)  # Показываю объявления с количеством комнат не меньше указанного

        # Фильтрация по типу недвижимости
        if property_type:
            queryset = queryset.filter(property_type__icontains=property_type)  # Фильтрую по типу недвижимости

        # Сортировка
        if sort_by in ['title', 'price', 'created_at']:  # Проверяю, что поле для сортировки корректное
            if order == 'asc':
                queryset = queryset.order_by(sort_by)  # Сортирую по возрастанию
            else:
                queryset = queryset.order_by(f'-{sort_by}')  # Сортирую по убыванию

        return queryset  # Возвращаю отсортированный и отфильтрованный список объявлений

# Класс для поиска объявлений по заголовку
# Я хочу дать возможность пользователю искать объявления по ключевым словам
class Search(ListView):
    template_name = 'user/all_listings.html'
    context_object_name = 'listings'
    paginate_by = 5  # Показываю по 5 объявлений на странице

    def get_queryset(self):
        # Ищу объявления, которые соответствуют запросу пользователя
        return Listing.objects.filter(title__iregex=self.request.GET.get('q'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')  # Добавляю запрос в контекст, чтобы показать его на странице
        return context
