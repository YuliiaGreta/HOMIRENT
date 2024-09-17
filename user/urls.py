from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('homepage/', views.homepage, name='homepage'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('items/', views.ListingListView.as_view(), name='view_listings'),
    path('homepage/<int:user_id>/', views.user_homepage, name='user_homepage'),
    path('search/', views.Search.as_view(), name='search')

]