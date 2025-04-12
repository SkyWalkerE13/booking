from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('hotels/', views.hotels, name='hotels'),
    path('hotels/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('hotels/<int:hotel_id>/rooms/', views.hotel_rooms, name='hotel_rooms'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('rooms/<int:room_id>/book/', views.book_room, name='book_room'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('search/', views.search_rooms, name='search_rooms'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # ... другие URL-маршруты
] 