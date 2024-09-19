from django.urls import path
from . import views

app_name = 'user'  # Я задаю пространство имен для URL, чтобы можно было легко ссылаться на маршруты в приложении "user"

# Список маршрутов для приложения "user"
urlpatterns = [
    path('register/', views.register, name='register'),  # URL для страницы регистрации нового пользователя
    path('homepage/', views.homepage, name='homepage'),  # URL для домашней страницы, куда попадает пользователь после входа
    path('logout/', views.user_logout, name='logout'),  # URL для выхода из аккаунта, чтобы пользователь могла завершить сессию
    path('login/', views.user_login, name='login'),  # URL для страницы входа в систему, где пользователь может ввести свои данные для входа
    path('items/', views.ListingListView.as_view(), name='view_listings'),  # URL для просмотра всех объявлений через ListView
    path('homepage/<int:user_id>/', views.user_homepage, name='user_homepage'),  # URL для домашней страницы конкретного пользователя по его ID
    path('search/', views.Search.as_view(), name='search'),  # URL для страницы поиска объявлений по ключевым словам
]
