from django.urls import path  # Импортирую path для создания маршрутов
from . import views  # Импортирую представления (views) для использования в маршрутах

app_name = 'booking'  # Указываю пространство имен для маршрутов, чтобы потом легче было к ним обращаться

urlpatterns = [
    path('list/', views.booking_list, name='booking_list'),  # Маршрут для просмотра списка всех бронирований пользователя
    path('cancel/<int:pk>/', views.cancel_booking, name='cancel_booking'),  # Маршрут для отмены конкретного бронирования
    path('confirm/<int:pk>/', views.confirm_booking, name='confirm_booking'),  # Маршрут для подтверждения бронирования арендодателем
    path('landlord/', views.landlord_booking_list, name='landlord_booking_list'),  # Маршрут для просмотра списка бронирований арендодателя
    path('new/<int:listing_id>/', views.create_booking, name='create_booking'),  # Маршрут для создания нового бронирования для конкретного объявления
]
