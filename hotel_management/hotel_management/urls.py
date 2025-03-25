from django.urls import path
from booking import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Добавляем URL для медиа-файлов в режиме разработки
urlpatterns = [
    # Публичные URL
    path('admin/', admin.site.urls),  # Встроенная админка Django
    #path('', include('booking.urls')),  # URL из нашего приложения
    path('accounts/', include('django.contrib.auth.urls')),  # URL для авторизации
    path('', views.home, name='home'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('rooms/<int:room_id>/book/', views.book_room, name='book_room'),
    
    # URL для авторизованных пользователей
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('bookings/<uuid:booking_id>/', views.booking_detail, name='booking_detail'),
    path('bookings/<uuid:booking_id>/payment/', views.payment_process, name='payment_process'),
    path('bookings/<uuid:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    
    # URL для администраторов
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/rooms/', views.manage_rooms, name='manage_rooms'),
    path('admin/bookings/', views.manage_bookings, name='manage_bookings'),
    path('admin/reports/', views.generate_reports, name='generate_reports'),

    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)