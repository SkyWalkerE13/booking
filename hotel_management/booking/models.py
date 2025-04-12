from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from django.db import models

class Hotel(models.Model):
    """Модель отеля"""
    name = models.CharField(max_length=200, verbose_name='Название')
    address = models.CharField(max_length=500, verbose_name='Адрес')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Цена за ночь')
    description = models.TextField(verbose_name='Описание')
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0,
        verbose_name='Рейтинг'
    )
    image = models.ImageField(
        upload_to='hotels/',
        null=True,
        blank=True,
        verbose_name='Изображение'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'
        ordering = ['-rating', 'name']

    def __str__(self):
        return self.name

    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0
        
class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Одноместный'),
        ('double', 'Двухместный'),
        ('suite', 'Люкс'),
    ]

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    number = models.CharField(max_length=10, verbose_name='Номер комнаты')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, verbose_name='Тип номера')
    description = models.TextField(verbose_name='Описание')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за ночь')
    capacity = models.PositiveIntegerField(verbose_name='Вместимость')
    available = models.BooleanField(default=True, verbose_name='Доступен')
    image = models.ImageField(upload_to='room_images/')
    image = models.ImageField(
        upload_to='rooms/',
        null=True,
        blank=True,
        verbose_name='Изображение',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'
        unique_together = ['hotel', 'number']

    def __str__(self):
        return f"{self.hotel.name} - Номер {self.number}"

class Booking(models.Model):
    BOOKING_STATUS = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
        ('completed', 'Завершено'),
        ('checked_in', 'Заселен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='bookings')
    booking_id = models.UUIDField(default=uuid.uuid4, unique=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    def __str__(self):
        return f"Бронирование {self.booking_id}"

class Payment(models.Model):
    """Модель для платежей"""
    PAYMENT_METHODS = (
        ('credit_card', 'Кредитная карта'),
        ('debit_card', 'Дебетовая карта'),
        ('bank_transfer', 'Банковский перевод'),
        ('cash', 'Наличные'),
    )

    PAYMENT_STATUS = (
        ('pending', 'Ожидает обработки'),
        ('completed', 'Завершен'),
        ('failed', 'Ошибка'),
        ('refunded', 'Возмещен'),
    )

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, verbose_name="Бронирование")
    payment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="ID платежа")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    payment_date = models.DateTimeField(default=timezone.now, verbose_name="Дата платежа")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, verbose_name="Способ оплаты")
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending', verbose_name="Статус")
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name="ID транзакции")

    def __str__(self):
        return f"Платеж {self.payment_id} для бронирования {self.booking.booking_id}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

class Review(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('room', 'user')  # Один пользователь может оставить только один отзыв на комнату

    def __str__(self):
        return f"Отзыв от {self.user.username} о {self.room.number}"  # изменено с room.name на room.number