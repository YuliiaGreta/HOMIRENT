from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.booking_list, name='booking_list'),  # Список бронирований
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),  # Отмена бронирования
    path('confirm/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),  # Подтверждение бронирования
    path('new/<int:listing_id>/', views.create_booking, name='create_booking'),  # Создание нового бронирования
    # path('notifications/', views.notifications_list, name='notifications_list'),  # Просмотр уведомлений
]
