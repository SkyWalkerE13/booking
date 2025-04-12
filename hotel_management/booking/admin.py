from django.contrib import admin
from booking.models import Hotel, Room, Booking

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'rating')
    search_fields = ('name', 'address')
    list_filter = ('rating',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'number', 'room_type', 'price_per_night', 'capacity', 'available')
    list_filter = ('hotel', 'room_type', 'available')
    search_fields = ('number', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in_date', 'check_out_date', 'status', 'total_price')  # исправлено!
    list_filter = ('status', 'check_in_date', 'check_out_date')  # исправлено!
    search_fields = ('user__username', 'room__number')
    date_hierarchy = 'check_in_date'  # исправлено!
