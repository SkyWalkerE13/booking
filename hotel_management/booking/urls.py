from django.contrib import admin
from django.urls import path, include
from . import views as booking_views


# URL для административной панели
admin_patterns = [
    path('dashboard/', booking_views.admin_dashboard, name='admin_dashboard'),
    path('bookings/', booking_views.admin_bookings, name='admin_bookings'),
    path('bookings/<int:booking_id>/', booking_views.admin_booking_detail, name='admin_booking_detail'),
    path('bookings/<int:booking_id>/confirm/', booking_views.admin_booking_confirm, name='admin_booking_confirm'),
    path('bookings/<int:booking_id>/cancel/', booking_views.admin_booking_cancel, name='admin_booking_cancel'),
    path('bookings/<int:booking_id>/complete/', booking_views.admin_booking_complete, name='admin_booking_complete'),
    path('hotels/', booking_views.admin_hotels, name='admin_hotels'),
    path('hotels/add/', booking_views.admin_hotel_add, name='admin_hotel_add'),
    path('hotels/<int:hotel_id>/edit/', booking_views.admin_hotel_edit, name='admin_hotel_edit'),
    path('rooms/', booking_views.admin_rooms, name='admin_rooms'),
    path('rooms/add/', booking_views.admin_room_add, name='admin_room_add'),
    path('rooms/<int:room_id>/edit/', booking_views.admin_room_edit, name='admin_room_edit'),
    path('rooms/<int:room_id>/toggle-availability/', booking_views.admin_room_toggle_availability, name='admin_room_toggle_availability'),
    path('users/', booking_views.admin_users, name='admin_users'),
    path('users/<int:user_id>/', booking_views.admin_user_detail, name='admin_user_detail'),
    path('users/<int:user_id>/edit/', booking_views.admin_user_edit, name='admin_user_edit'),
    path('users/<int:user_id>/toggle-active/', booking_views.admin_user_toggle_active, name='admin_user_toggle_active'),
    path('users/<int:user_id>/toggle-staff/', booking_views.admin_user_toggle_staff, name='admin_user_toggle_staff'),
    path('reviews/', booking_views.admin_reviews, name='admin_reviews'),
    path('reports/', booking_views.admin_reports, name='admin_reports'),
]

# Основные URL приложения
urlpatterns = [
    path('admin-panel/', include(admin_patterns)),
    path('index/', booking_views.index, name='index'),
    path('about/', booking_views.about, name='about'),
    path('contact/', booking_views.contact, name='contact'),
    path('contact/destination.html', booking_views.destination, name='destination'),
    path('search/', booking_views.search_rooms, name='search_rooms'),
    path('', booking_views.home, name='home'),
    path('rooms/', booking_views.room_list, name='room_list'),
    path('rooms/<int:room_id>/', booking_views.room_detail, name='room_detail'),
    path('rooms/<int:room_id>/book/', booking_views.book_room, name='book_room'),
    path('hotels/', booking_views.hotels, name='hotels'),
    path('hotels/<int:hotel_id>/', booking_views.hotel_detail, name='hotel_detail'),
    path('hotels/<int:hotel_id>/rooms/', booking_views.hotel_rooms, name='hotel_rooms'),
    path('register/', booking_views.register, name='register'),
    path('login/', booking_views.login_view, name='login'),
    path('logout/', booking_views.logout_view, name='logout'),
    path('bookings/', booking_views.my_bookings, name='my_bookings'),
    path('bookings/<uuid:booking_id>/', booking_views.booking_detail, name='booking_detail'),
    path('bookings/<uuid:booking_id>/payment/', booking_views.payment_process, name='payment_process'),
    path('bookings/<uuid:booking_id>/cancel/', booking_views.cancel_booking, name='cancel_booking'),
    path('room/<slug:slug>/review/', booking_views.add_review, name='add_review'),
]
