from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class Room(models.Model):
    """Модель для номеров отеля"""
    ROOM_TYPES = (
        ('single', 'Одноместный'),
        ('double', 'Двухместный'),
        ('suite', 'Люкс'),
        ('family', 'Семейный'),
        ('deluxe', 'Делюкс'),
    )

    number = models.CharField(max_length=10, unique=True, verbose_name="Номер комнаты")
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, verbose_name="Тип номера")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за ночь")
    capacity = models.PositiveSmallIntegerField(default=1, verbose_name="Вместимость")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_available = models.BooleanField(default=True, verbose_name="Доступен")

    def __str__(self):
        return f"{self.get_room_type_display()} номер {self.number}"

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"


class RoomImage(models.Model):
    """Модель для изображений номеров"""
    room = models.ForeignKey(Room, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room_images', verbose_name="Изображение")
    caption = models.CharField(max_length=100, blank=True, verbose_name="Подпись")

    def __str__(self):
        return f"Изображение для {self.room.number}"


class Booking(models.Model):
    """Модель для бронирований"""
    STATUS_CHOICES = (
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('checked_in', 'Заезд выполнен'),
        ('checked_out', 'Выезд выполнен'),
        ('cancelled', 'Отменено'),
    )

    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="ID бронирования")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Номер")
    guest = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Гость")
    check_in_date = models.DateField(verbose_name="Дата заезда")
    check_out_date = models.DateField(verbose_name="Дата выезда")
    adults = models.PositiveSmallIntegerField(default=1, verbose_name="Взрослых")
    children = models.PositiveSmallIntegerField(default=0, verbose_name="Детей")
    booking_date = models.DateTimeField(default=timezone.now, verbose_name="Дата бронирования")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    special_requests = models.TextField(blank=True, verbose_name="Особые пожелания")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")

    def __str__(self):
        return f"Бронирование {self.booking_id} - {self.guest.get_full_name()}"

    def save(self, *args, **kwargs):
        if not self.total_price:
            # Расчет общей стоимости при создании бронирования
            days = (self.check_out_date - self.check_in_date).days
            self.total_price = self.room.price_per_night * days
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"


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
