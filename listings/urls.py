from django.urls import path
from . import views  # Я импортирую все представления (views), которые будут обрабатываться в этом приложении

app_name = 'listings'  # Я задаю пространство имен для приложения 'listings', чтобы можно было легко ссылаться на его URL-адреса

# Список маршрутов (URL-путей) для работы с объявлениями
urlpatterns = [
    path('detail/<int:pk>/', views.listing_detail, name='listing_detail'),  # Путь для просмотра подробностей объявления по его ID
    path('new/', views.create_listing, name='create_listing'),  # Путь для создания нового объявления
    path('<int:pk>/edit/', views.edit_listing, name='edit_listing'),  # Путь для редактирования существующего объявления
    path('<int:pk>/delete/', views.delete_listing, name='delete_listing'),  # Путь для удаления объявления
    path('<int:pk>/', views.listing_detail, name='listing_detail'),  # Повторный путь для просмотра объявления (дубликат, можно удалить)
    path('viewall/', views.view_all_listings, name='view_all_listings'),  # Путь для просмотра всех объявлений
    path('my/', views.view_my_listings, name='my_listings'),  # Путь для просмотра только своих объявлений
    path('listing/<int:listing_id>/rate/', views.add_rating, name='add_rating'),  # Путь для добавления рейтинга к объявлению
    path('listing/<int:pk>/reviews/', views.listing_reviews, name='listing_reviews'),  # Путь для просмотра всех отзывов для конкретного объявления
    path('listings/', views.view_all_listings, name='listings_list'),  # Путь для отображения списка всех объявлений
    path('', views.home, name='home'),  # Главная страница приложения объявлений
    path('listing/<int:listing_id>/toggle-status/', views.toggle_listing_status, name='toggle_listing_status'),  # Путь для изменения статуса объявления (активно/неактивно)
]
