from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('history/', views.search_history, name='search_history'),
    path('viewed/', views.view_history, name='view_history'),
]

