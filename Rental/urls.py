from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('listings.urls')),  # Для API объявлений
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', include('user.urls')),  # Для приложения user
    path('booking/', include('booking.urls')),  # Бронирования
    path('search/', include('search.urls')),
    path('listings/', include('listings.urls')), # Поиск

]
