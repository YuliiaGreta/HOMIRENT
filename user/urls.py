from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('homepage/', views.homepage, name='homepage'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('listings/', views.view_listings, name='listings'),

]